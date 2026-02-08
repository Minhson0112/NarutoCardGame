import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import traceback

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.gachaPityCounterRepository import GachaPityCounterRepository

from bot.config.gachaConfig import GACHA_DROP_RATE, GACHA_PRICES, PITY_LIMIT, PITY_PROTECTION
from bot.config.weaponGachaConfig import WEAPON_GACHA_PRICES, WEAPON_GACHA_DROP_RATE, WEAPON_GACHA_PACKS
from bot.services.i18n import t


class ShopSwitchView(View):
    def __init__(self, guild_id, player_id, coin, pity_repo, author):
        super().__init__(timeout=300)
        self.author = author
        self.guild_id = guild_id
        self.player_id = player_id
        self.coin = coin
        self.pity_repo = pity_repo
        self.mode = "cards"  # "cards" | "weapons"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    def build_card_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=t(self.guild_id, "shop.title.cards"),
            description=t(self.guild_id, "shop.balance", coin=self.coin),
            color=discord.Color.blue()
        )

        packs = list(GACHA_DROP_RATE.items())
        for i, (pack, rates) in enumerate(packs):
            price = GACHA_PRICES[pack]
            pity_limit = PITY_LIMIT[pack]
            protection = PITY_PROTECTION[pack]
            current_count = self.pity_repo.getCount(self.player_id, pack)
            left = max(0, pity_limit - current_count)

            rate_lines = [
                t(self.guild_id, "shop.field.rates.line", tier=tier, percent=percent)
                for tier, percent in rates.items()
            ]
            rate_text = "\n".join(rate_lines) if rate_lines else t(self.guild_id, "shop.field.rates.empty")

            value_lines = [
                t(self.guild_id, "shop.field.price", price=price),
                t(self.guild_id, "shop.field.rates.title"),
                rate_text,
                t(self.guild_id, "shop.field.pity", left=left, protection=protection),
                t(self.guild_id, "shop.field.buy.card", pack=pack),
            ]
            value = "\n".join(value_lines)

            embed.add_field(
                name=t(self.guild_id, "shop.pack.name", pack=pack),
                value=value,
                inline=False
            )

            if i != len(packs) - 1:
                embed.add_field(
                    name="\u200b",
                    value=t(self.guild_id, "shop.pack.separator"),
                    inline=False
                )

        embed.set_footer(text=t(self.guild_id, "shop.footer.cards"))
        return embed

    def build_weapon_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=t(self.guild_id, "shop.title.weapons"),
            description=t(self.guild_id, "shop.balance", coin=self.coin),
            color=discord.Color.blue()
        )

        packs = list(WEAPON_GACHA_PACKS)
        for i, pack in enumerate(packs):
            price = WEAPON_GACHA_PRICES.get(pack, 0)
            rates = WEAPON_GACHA_DROP_RATE.get(pack, {})

            rate_lines = [
                t(self.guild_id, "shop.field.rates.line", tier=tier, percent=percent)
                for tier, percent in rates.items()
            ]
            rate_text = "\n".join(rate_lines) if rate_lines else t(self.guild_id, "shop.field.rates.empty")

            value_lines = [
                t(self.guild_id, "shop.field.price", price=price),
                t(self.guild_id, "shop.field.rates.title"),
                rate_text,
                t(self.guild_id, "shop.field.buy.weapon", pack=pack),
            ]
            value = "\n".join(value_lines)

            embed.add_field(
                name=t(self.guild_id, "shop.pack.name", pack=pack),
                value=value,
                inline=False
            )

            if i != len(packs) - 1:
                embed.add_field(
                    name="\u200b",
                    value=t(self.guild_id, "shop.pack.separator"),
                    inline=False
                )

        embed.set_footer(text=t(self.guild_id, "shop.footer.weapons"))
        return embed

    def build_embed(self) -> discord.Embed:
        return self.build_card_embed() if self.mode == "cards" else self.build_weapon_embed()

    def sync_button_label(self, button: Button) -> None:
        if self.mode == "cards":
            button.label = t(self.guild_id, "shop.button.to_weapons")
        else:
            button.label = t(self.guild_id, "shop.button.to_cards")

    @discord.ui.button(label="...", style=discord.ButtonStyle.secondary)
    async def switch_shop(self, interaction: discord.Interaction, button: Button):
        self.mode = "weapons" if self.mode == "cards" else "cards"
        self.sync_button_label(button)
        await interaction.response.edit_message(embed=self.build_embed(), view=self)

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = True


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shop", description="Xem cửa hàng (thẻ / vũ khí)")
    async def shop(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                player_repo = PlayerRepository(session)
                pity_repo = GachaPityCounterRepository(session)

                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send(t(guild_id, "shop.not_registered"))
                    return

                view = ShopSwitchView(
                    guild_id=guild_id,
                    player_id=player_id,
                    coin=player.coin_balance,
                    pity_repo=pity_repo,
                    author=interaction.user
                )

                # set label nút ban đầu theo ngôn ngữ hiện tại
                for item in view.children:
                    if isinstance(item, Button):
                        view.sync_button_label(item)
                        break

                await interaction.followup.send(embed=view.build_embed(), view=view)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(
                t(guild_id, "shop.error", error=tb),
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Shop(bot))
