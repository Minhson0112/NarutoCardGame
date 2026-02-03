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


SEPARATOR_LINE = "━━━━━━━━━━━━━━━━━━"


class ShopSwitchView(View):
    def __init__(self, player_id, coin, pity_repo, author):
        super().__init__(timeout=300)
        self.author = author
        self.player_id = player_id
        self.coin = coin
        self.pity_repo = pity_repo
        self.mode = "cards"  # "cards" | "weapons"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    def build_card_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="🛒 Shop Thẻ Bài",
            description=f"💰 Số dư của bạn: **{self.coin:,} Ryo**",
            color=discord.Color.blue()
        )

        packs = list(GACHA_DROP_RATE.items())
        for i, (pack, rates) in enumerate(packs):
            price = GACHA_PRICES[pack]
            pity_limit = PITY_LIMIT[pack]
            protection = PITY_PROTECTION[pack]
            current_count = self.pity_repo.getCount(self.player_id, pack)
            left = max(0, pity_limit - current_count)

            rate_lines = [f"• **{tier}**: {percent}%" for tier, percent in rates.items()]
            rate_text = "\n".join(rate_lines) if rate_lines else "• Không có cấu hình tỉ lệ."

            value = (
                f"**Giá:** {price:,} Ryo\n"
                f"**Tỉ lệ:**\n{rate_text}\n"
                f"**Bảo hiểm:** Còn **{left}** lần để đảm bảo nhận **{protection}**\n"
                f"**Mua:** `/buycard pack:{pack}`"
            )

            embed.add_field(
                name=f"📦 **{pack}**",
                value=value,
                inline=False
            )

            if i != len(packs) - 1:
                embed.add_field(name="\u200b", value=SEPARATOR_LINE, inline=False)

        embed.set_footer(text="Shop Thẻ Bài")
        return embed

    def build_weapon_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="🛒 Shop Vũ Khí",
            description=f"💰 Số dư của bạn: **{self.coin:,} Ryo**",
            color=discord.Color.blue()
        )

        packs = list(WEAPON_GACHA_PACKS)
        for i, pack in enumerate(packs):
            price = WEAPON_GACHA_PRICES.get(pack, 0)
            rates = WEAPON_GACHA_DROP_RATE.get(pack, {})

            rate_lines = [f"• **{tier}**: {percent}%" for tier, percent in rates.items()]
            rate_text = "\n".join(rate_lines) if rate_lines else "• Không có cấu hình tỉ lệ."

            value = (
                f"**Giá:** {price:,} Ryo\n"
                f"**Tỉ lệ:**\n{rate_text}\n"
                f"**Mua:** `/buyweapon pack:{pack}`"
            )

            embed.add_field(
                name=f"📦 **{pack}**",
                value=value,
                inline=False
            )

            if i != len(packs) - 1:
                embed.add_field(name="\u200b", value=SEPARATOR_LINE, inline=False)

        embed.set_footer(text="Shop Vũ Khí")
        return embed

    def build_embed(self) -> discord.Embed:
        return self.build_card_embed() if self.mode == "cards" else self.build_weapon_embed()

    def sync_button_label(self, button: Button) -> None:
        button.label = "Shop vũ khí" if self.mode == "cards" else "Shop thẻ"

    @discord.ui.button(label="Shop vũ khí", style=discord.ButtonStyle.secondary)
    async def switch_shop(self, interaction: discord.Interaction, button: Button):
        self.mode = "weapons" if self.mode == "cards" else "cards"
        self.sync_button_label(button)
        await interaction.response.edit_message(embed=self.build_embed(), view=self)


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shop", description="Xem cửa hàng (thẻ / vũ khí)")
    async def shop(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                player_repo = PlayerRepository(session)
                pity_repo = GachaPityCounterRepository(session)

                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!")
                    return

                view = ShopSwitchView(
                    player_id=player_id,
                    coin=player.coin_balance,
                    pity_repo=pity_repo,
                    author=interaction.user
                )

                await interaction.followup.send(embed=view.build_embed(), view=view)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(f"❌ Có lỗi xảy ra:\n```{tb}```", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Shop(bot))
