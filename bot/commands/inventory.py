import math
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import traceback

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.services.help import get_card_effective_stats, get_weapon_effective_stats
from bot.services.i18n import t

ITEMS_PER_PAGE = 4


def _localize_buff_label(guild_id: int | None, key_name: str) -> str:
    mapping = {
        "damage": "inventory.buff.damage",
        "health": "inventory.buff.health",
        "armor": "inventory.buff.armor",
        "crit_rate": "inventory.buff.crit_rate",
        "speed": "inventory.buff.speed",
        "chakra": "inventory.buff.chakra",
    }
    lang_key = mapping.get(key_name)
    if not lang_key:
        return key_name.replace("_", " ").title()
    return t(guild_id, lang_key)


class InventoryView(View):
    def __init__(self, guild_id: int | None, cards, weapons, author):
        super().__init__(timeout=300)
        self.guild_id = guild_id
        self.author = author

        self.cards = sorted(
            cards,
            key=lambda c: get_card_effective_stats(c)["strength"],
            reverse=True
        )
        self.weapons = weapons

        self.mode = "cards"
        self.current_page = 0

        self._sync_button_labels()

    def _get_button(self, custom_id: str) -> Button | None:
        for child in self.children:
            if isinstance(child, Button) and child.custom_id == custom_id:
                return child
        return None

    def _sync_button_labels(self) -> None:
        prev_btn = self._get_button("inventory.prev")
        next_btn = self._get_button_button("inventory.next") if False else None  # placeholder to avoid lint tools

        next_btn = self._get_button("inventory.next")
        toggle_btn = self._get_button("inventory.toggle")

        if prev_btn:
            prev_btn.label = t(self.guild_id, "inventory.button.prev")
        if next_btn:
            next_btn.label = t(self.guild_id, "inventory.button.next")
        if toggle_btn:
            self._sync_toggle_button_label(toggle_btn)

    def _sync_toggle_button_label(self, button: Button) -> None:
        if self.mode == "cards":
            button.label = t(self.guild_id, "inventory.button.to_weapons")
        else:
            button.label = t(self.guild_id, "inventory.button.to_cards")

    def get_total_pages(self) -> int:
        data = self.cards if self.mode == "cards" else self.weapons
        return math.ceil(len(data) / ITEMS_PER_PAGE) if data else 1

    def build_embed(self) -> discord.Embed:
        total_pages = self.get_total_pages()
        start = self.current_page * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        if self.mode == "cards":
            embed = discord.Embed(
                title=t(self.guild_id, "inventory.embed.cards.title"),
                color=discord.Color.green()
            )
            subset = self.cards[start:end]

            if subset:
                lines = []
                locked_marker = t(self.guild_id, "inventory.card.locked_marker")
                for card in subset:
                    name_line = f"•🥷 **{card.template.name}** (Lv {card.level})"
                    if card.locked:
                        name_line += locked_marker
                    name_line += "\n"

                    lines.append(
                        f"{name_line}"
                        f"  ┣ **{t(self.guild_id, 'inventory.field.id')}:** `{card.id}`\n"
                        f"  ┣ **{t(self.guild_id, 'inventory.field.tier')}:** {card.template.tier}\n"
                        f"  ┣ **{t(self.guild_id, 'inventory.field.tanker')}:** {'✅' if card.template.first_position else '❌'}\n"
                        f"  ┗ **{t(self.guild_id, 'inventory.field.quantity')}:** {card.quantity}\n"
                    )
                embed.description = "\n".join(lines).strip()
            else:
                embed.description = t(self.guild_id, "inventory.embed.cards.empty")

        else:
            embed = discord.Embed(
                title=t(self.guild_id, "inventory.embed.weapons.title"),
                color=discord.Color.purple()
            )
            subset = self.weapons[start:end]

            if subset:
                lines = []
                for weapon in subset:
                    stats = get_weapon_effective_stats(weapon)
                    buffs = []
                    for k, v in stats.items():
                        if not v:
                            continue
                        key_name = k.replace("bonus_", "")
                        label = _localize_buff_label(self.guild_id, key_name)
                        val = f"{v:.0%}" if isinstance(v, float) else str(v)
                        buffs.append((label, val))

                    block = [
                        f"•🔪 **{weapon.template.name}** (Lv {weapon.level})",
                        f"  ┣ **{t(self.guild_id, 'inventory.field.id')}:** `{weapon.id}`",
                        f"  ┣ **{t(self.guild_id, 'inventory.field.grade')}:** {weapon.template.grade}",
                        f"  ┣ **{t(self.guild_id, 'inventory.field.quantity_weapon')}:** {weapon.quantity}",
                    ]

                    for i, (label, val) in enumerate(buffs):
                        bullet = "┗" if i == len(buffs) - 1 else "┣"
                        block.append(f"  {bullet} **{label}:** {val}")

                    lines.append("\n".join(block))

                embed.description = "\n\n".join(lines)
            else:
                embed.description = t(self.guild_id, "inventory.embed.weapons.empty")

        embed.set_footer(text=t(self.guild_id, "inventory.footer.page", page=self.current_page + 1, total=total_pages))
        return embed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, custom_id="inventory.prev")
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)
        else:
            await interaction.response.send_message(t(self.guild_id, "inventory.msg.first_page"), ephemeral=True)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, custom_id="inventory.next")
    async def next_page(self, interaction: discord.Interaction, button: Button):
        total_pages = self.get_total_pages()
        if self.current_page < total_pages - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)
        else:
            await interaction.response.send_message(t(self.guild_id, "inventory.msg.last_page"), ephemeral=True)

    @discord.ui.button(label="Toggle", style=discord.ButtonStyle.secondary, custom_id="inventory.toggle")
    async def toggle_inventory(self, interaction: discord.Interaction, button: Button):
        self.mode = "weapons" if self.mode == "cards" else "cards"

        total_pages = self.get_total_pages()
        if self.current_page >= total_pages:
            self.current_page = max(0, total_pages - 1)

        self._sync_toggle_button_label(button)
        await interaction.response.edit_message(embed=self.build_embed(), view=self)


class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="inventory", description="Inventory")
    async def inventory(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                player_repo = PlayerRepository(session)
                card_repo = PlayerCardRepository(session)
                weapon_repo = PlayerWeaponRepository(session)

                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'inventory.error.not_registered')}"
                    )
                    return

                cards = card_repo.getByPlayerId(player_id)
                weapons = weapon_repo.getByPlayerId(player_id)

                view = InventoryView(guild_id, cards, weapons, interaction.user)
                await interaction.followup.send(embed=view.build_embed(), view=view)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(
                f"❌ Có lỗi xảy ra:\n```{tb}```",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Inventory(bot))
