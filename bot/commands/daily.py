import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyClaimLogRepository import DailyClaimLogRepository
from bot.services.playerService import PlayerService

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="daily", description="Nhận 10,000 ryo mỗi ngày")
    async def daily(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                claimRepo = DailyClaimLogRepository(session)
                playerService = PlayerService(playerRepo)

                if claimRepo.hasClaimedToday(playerId):
                    await interaction.followup.send("❗ Bạn đã nhận thưởng hôm nay rồi. Quay lại vào ngày mai nhé!")
                    return

                # Cộng 10,000 ryo
                if not playerService.addCoin(playerId, 10000):
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Dùng `/register` trước nhé!")
                    return

                # Đánh dấu đã nhận
                claimRepo.markClaimed(playerId)

                await interaction.followup.send("💰 Bạn đã nhận 10,000 ryo từ thưởng hàng ngày! Hẹn gặp lại mai nhé 😄")
        except Exception as e:
            print("❌ Lỗi khi xử lý daily:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Daily(bot))
