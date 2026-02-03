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

ITEMS_PER_PAGE = 4

class InventoryView(View):
    def __init__(self, cards, weapons, author):
        super().__init__(timeout=300)
        self.author = author

        self.cards = sorted(
            cards,
            key=lambda c: get_card_effective_stats(c)["strength"],
            reverse=True
        )
        self.weapons = weapons

        self.mode = "cards"
        self.current_page = 0

    def get_total_pages(self) -> int:
        data = self.cards if self.mode == "cards" else self.weapons
        return math.ceil(len(data) / ITEMS_PER_PAGE) if data else 1

    def build_embed(self) -> discord.Embed:
        total_pages = self.get_total_pages()
        start = self.current_page * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        if self.mode == "cards":
            embed = discord.Embed(title="🎴 Kho Thẻ Bài", color=discord.Color.green())
            subset = self.cards[start:end]

            if subset:
                lines = []
                for card in subset:
                    stats = get_card_effective_stats(card)
                    nameMsg = (
                        f"•🥷 **{card.template.name}** (Lv {card.level}) (🔒)\n"
                        if card.locked
                        else f"•🥷 **{card.template.name}** (Lv {card.level})\n"
                    )
                    lines.append(
                        f"{nameMsg}"
                        f"  ┣ **ID:** `{card.id}`\n"
                        f"  ┣ **Bậc:** {card.template.tier}\n"
                        f"  ┣ **Tanker:** {'✅' if card.template.first_position else '❌'}\n"
                        f"  ┗ **Số Lượng:** {card.quantity}\n"
                    )
                embed.description = "\n\n".join(lines)
            else:
                embed.description = "Không có thẻ nào."

        else:
            embed = discord.Embed(title="🔪 Kho Vũ Khí", color=discord.Color.purple())
            subset = self.weapons[start:end]

            if subset:
                lines = []
                for weapon in subset:
                    stats = get_weapon_effective_stats(weapon)
                    buffs = [
                        (
                            k.replace("bonus_", "").replace("_", " ").title(),
                            f"{v:.0%}" if isinstance(v, float) else str(v)
                        )
                        for k, v in stats.items() if v
                    ]

                    block = [
                        f"•🔪 **{weapon.template.name}** (Lv {weapon.level})",
                        f"  ┣ **ID:** `{weapon.id}`",
                        f"  ┣ **Bậc:** {weapon.template.grade}",
                        f"  ┣ **Số Lượng:** {weapon.quantity}"
                    ]

                    for i, (label, val) in enumerate(buffs):
                        bullet = "┗" if i == len(buffs) - 1 else "┣"
                        block.append(f"  {bullet} **{label}:** {val}")

                    lines.append("\n".join(block))

                embed.description = "\n\n".join(lines)
            else:
                embed.description = "Không có vũ khí nào."

        embed.set_footer(text=f"Trang {self.current_page + 1}/{total_pages}")
        return embed

    def sync_toggle_button_label(self, button: Button) -> None:
        if self.mode == "cards":
            button.label = "Kho vũ khí"
        else:
            button.label = "Kho thẻ"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)
        else:
            await interaction.response.send_message("Bạn đang ở trang đầu!", ephemeral=True)

    @discord.ui.button(label="Tiếp", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        total_pages = self.get_total_pages()
        if self.current_page < total_pages - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)
        else:
            await interaction.response.send_message("Bạn đang ở trang cuối!", ephemeral=True)

    @discord.ui.button(label="Kho vũ khí", style=discord.ButtonStyle.secondary)
    async def toggle_inventory(self, interaction: discord.Interaction, button: Button):
        self.mode = "weapons" if self.mode == "cards" else "cards"

        total_pages = self.get_total_pages()
        if self.current_page >= total_pages:
            self.current_page = max(0, total_pages - 1)

        self.sync_toggle_button_label(button)
        await interaction.response.edit_message(embed=self.build_embed(), view=self)


class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="inventory", description="Hiển thị kho đồ của bạn")
    async def inventory(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                player_repo = PlayerRepository(session)
                card_repo = PlayerCardRepository(session)
                weapon_repo = PlayerWeaponRepository(session)

                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!"
                    )
                    return

                cards = card_repo.getByPlayerId(player_id)
                weapons = weapon_repo.getByPlayerId(player_id)

                view = InventoryView(cards, weapons, interaction.user)
                await interaction.followup.send(embed=view.build_embed(), view=view)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(
                f"❌ Có lỗi xảy ra:\n```{tb}```",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Inventory(bot))
