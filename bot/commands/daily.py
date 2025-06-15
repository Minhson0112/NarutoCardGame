import discord
from discord.ext import commands
from discord import app_commands
from datetime import date, timedelta

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyClaimLogRepository import DailyClaimLogRepository

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="daily", description="Nhận thưởng điểm danh hàng ngày")
    async def daily(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                claimRepo  = DailyClaimLogRepository(session)

                # Kiểm tra đã nhận hôm nay chưa
                if claimRepo.hasClaimedToday(playerId):
                    await interaction.followup.send(
                        "❗ Bạn đã nhận thưởng hôm nay rồi. Quay lại vào ngày mai nhé!"
                    )
                    return

                # Lấy player
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Dùng `/register` trước nhé!"
                    )
                    return

                # Tính số ngày liên tiếp
                today = date.today()
                yesterday = today - timedelta(days=1)
                last_date = claimRepo.getLastClaimDate(playerId)

                if last_date == yesterday:
                    player.consecutive_streak += 1
                else:
                    player.consecutive_streak = 1

                # Quay vòng sau 7 ngày
                if player.consecutive_streak > 7:
                    player.consecutive_streak = 1

                # Tính thưởng
                reward = player.consecutive_streak * 50000
                player.coin_balance += reward

                # Cập nhật player và đánh dấu đã nhận
                claimRepo.markClaimed(playerId)
                session.commit()

                await interaction.followup.send(
                    f"💰 Bạn đã nhận **{reward:,} ryo** (Chuỗi {player.consecutive_streak} ngày)! Hẹn gặp lại mai nhé 😄"
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý daily:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra. Vui lòng thử lại sau."
            )

async def setup(bot):
    await bot.add_cog(Daily(bot))
