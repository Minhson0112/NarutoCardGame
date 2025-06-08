import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.config.config import ADMIN_OVERRIDE_ID
from bot.repository.playerRepository import PlayerRepository
from bot.entity.player import Player

class ResetRank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="resetrank",
        description="(Dev only) Reset điểm rank, chuỗi thắng và trao thưởng Top10"
    )
    async def resetrank(self, interaction: discord.Interaction):
        # 1. Kiểm tra quyền
        if interaction.user.id not in ADMIN_OVERRIDE_ID:
            await interaction.response.send_message(
                "❌ Bạn không có quyền sử dụng lệnh này.",
                ephemeral=True
            )
            return

        await interaction.response.defer(thinking=True)
        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                topPlayers = playerRepo.getTop10()

                # 2. Tính phần thưởng cho Top10
                description = ""
                for idx, player in enumerate(topPlayers, start=1):
                    old_points = player.rank_points
                    award_value = (11 - idx) * 100_000
                    player.coin_balance += award_value
                    reward_str = "1m" if award_value >= 1_000_000 else f"{award_value // 1_000}k"
                    description += (
                        f"🏆 **Top {idx}. {player.username}** – "
                        f"điểm rank: {old_points} – đã nhận **{reward_str}** ryo\n"
                    )

                session.query(Player).update(
                    {Player.rank_points: 0, Player.winning_streak: 0},
                    synchronize_session=False
                )
                session.commit()

            # 4. Gửi embed thông báo
            embed = discord.Embed(
                title="🎉 **Thông Báo Reset Điểm Rank**",
                description=description,
                color=discord.Color.green()
            )
            embed.set_footer(
                text="✅ Đã reset điểm rank và chuỗi thắng về 0 cho tất cả người chơi."
            )
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý /resetrank:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra. Vui lòng thử lại sau."
            )

async def setup(bot):
    await bot.add_cog(ResetRank(bot))