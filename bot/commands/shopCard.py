import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.gachaPityCounterRepository import GachaPityCounterRepository
from bot.config.gachaConfig import GACHA_DROP_RATE, GACHA_PRICES, PITY_LIMIT, PITY_PROTECTION

class ShopCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shopcard", description="Xem cửa hàng thẻ bài")
    async def shopCard(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                pityRepo = GachaPityCounterRepository(session)
                
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!")
                    return

                coin = player.coin_balance
                embed = discord.Embed(
                    title="🛒 Shop Thẻ Bài",
                    description=f"💰 Số dư của bạn: **{coin:,} Ryo**",
                    color=discord.Color.blue()
                )
                
                # Lặp qua các gói mở thẻ được cấu hình trong gachaConfig
                for pack, rates in GACHA_DROP_RATE.items():
                    price = GACHA_PRICES[pack]
                    pityLimit = PITY_LIMIT[pack]
                    protection = PITY_PROTECTION[pack]
                    currentCount = pityRepo.getCount(playerId, pack)
                    left = max(0, pityLimit - currentCount)
                    
                    # Tạo chuỗi hiển thị drop rate
                    rateText = "\n".join([f"- {tier}: {percent}%" for tier, percent in rates.items()])
                    
                    embed.add_field(
                        name=f"\n\n\n📦 {pack} — Giá: {price:,} Ryo",
                        value=(
                            f"{rateText}\n"
                            f"🛡️ Còn {left} lần mua để đảm bảo nhận **{protection}**\n"
                            f"👉 Sử dụng lệnh `/buycard pack: {pack}` để mua\n\n\n"
                        ),
                        inline=False
                    )
                
                embed.set_footer(text="Shop Thẻ Bài - Đổi mới trải nghiệm, mở ra cơ hội nhận thẻ hiếm!")
                await interaction.followup.send(embed=embed)
        except Exception as e:
            print("❌ Lỗi khi xử lý shopcard:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(ShopCard(bot))
