import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.config.weaponGachaConfig import WEAPON_GACHA_PRICES, WEAPON_GACHA_DROP_RATE, WEAPON_GACHA_PACKS

class ShopWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shopweapon", description="Xem cửa hàng vũ khí")
    async def shopWeapon(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!")
                    return

                coin = player.coin_balance
                embed = discord.Embed(
                    title="🛒 Shop Vũ Khí",
                    description=f"💰 Số dư của bạn: **{coin:,} Ryo**",
                    color=discord.Color.blue()
                )
                
                # Lặp qua các gói mở vũ khí được cấu hình trong weaponGachaConfig
                for pack in WEAPON_GACHA_PACKS:
                    price = WEAPON_GACHA_PRICES.get(pack, 0)
                    rates = WEAPON_GACHA_DROP_RATE.get(pack, {})
                    rateText = "\n".join([f"- {tier}: {percent}%" for tier, percent in rates.items()])
                    
                    embed.add_field(
                        name=f"\n\n\n📦 {pack} — Giá: {price:,} Ryo",
                        value=(
                            f"{rateText}\n"
                            f"👉 Sử dụng lệnh `/buyweapon pack: {pack}` để mua\n\n\n"
                        ),
                        inline=False
                    )
                
                embed.set_footer(text="Shop Vũ Khí - Hãy lựa chọn vũ khí thích hợp cho tướng của bạn!")
                await interaction.followup.send(embed=embed)
        except Exception as e:
            print("❌ Lỗi khi xử lý shopweapon:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(ShopWeapon(bot))
