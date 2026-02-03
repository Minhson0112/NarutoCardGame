import discord
from discord.ext import commands
from discord import app_commands
from datetime import date, timedelta

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyClaimLogRepository import DailyClaimLogRepository
from bot.services.i18n import t


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="daily", description="Nhận thưởng điểm danh hàng ngày")
    async def daily(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        guild_id = interaction.guild.id if interaction.guild else None
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                claimRepo = DailyClaimLogRepository(session)

                if claimRepo.hasClaimedToday(player_id):
                    await interaction.followup.send(t(guild_id, "daily.already_claimed"))
                    return

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(t(guild_id, "daily.not_registered"))
                    return

                today = date.today()
                yesterday = today - timedelta(days=1)
                last_date = claimRepo.getLastClaimDate(player_id)

                if last_date == yesterday:
                    player.consecutive_streak += 1
                else:
                    player.consecutive_streak = 1

                if player.consecutive_streak > 7:
                    player.consecutive_streak = 1

                reward = player.consecutive_streak * 50000
                player.coin_balance += reward

                claimRepo.markClaimed(player_id)
                session.commit()

                await interaction.followup.send(
                    t(
                        guild_id,
                        "daily.success",
                        reward=reward,
                        streak=player.consecutive_streak
                    )
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý daily:", e)
            await interaction.followup.send(t(guild_id, "daily.error"))


async def setup(bot):
    await bot.add_cog(Daily(bot))
