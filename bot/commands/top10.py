import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository

class Top10(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="top10", description="Lấy bảng xếp hạng Top 10 theo điểm rank hiện tại")
    async def top10(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                # Lấy danh sách Top 10 người chơi theo điểm rank giảm dần
                topPlayers = playerRepo.getTop10()
                # Xác định thứ hạng của người dùng gọi lệnh
                myRank = playerRepo.getPlayerRank(interaction.user.id)

                # Xây dựng chuỗi bảng xếp hạng với emoji trang trí
                scoreboard = ""
                for idx, player in enumerate(topPlayers, start=1):
                    scoreboard += f"🏆 **{idx}. {player.username}** - {player.rank_points} điểm\n"

            embed = discord.Embed(
                title="BXH Điểm Rank Top 10 🔥",
                description=scoreboard,
                color=discord.Color.blue()
            )
            if myRank:
                embed.set_footer(text=f"🌟 Rank của bạn: {myRank}")
            else:
                embed.set_footer(text="❗ Bạn chưa có điểm rank.")

            await interaction.followup.send(embed=embed)
        except Exception as e:
            print("❌ Lỗi khi xử lý /top10:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Top10(bot))
