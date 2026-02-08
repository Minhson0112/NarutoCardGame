import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.services.i18n import t


class Top10(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="top10", description="Lấy bảng xếp hạng Top 10 theo điểm rank hiện tại")
    async def top10(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id if interaction.guild else None
        await interaction.response.defer(thinking=True)

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                topPlayers = playerRepo.getTop10()
                myRank = playerRepo.getPlayerRank(interaction.user.id)

            lines = []
            for idx, player in enumerate(topPlayers, start=1):
                lines.append(
                    t(
                        guild_id,
                        "top10.line",
                        idx=idx,
                        username=player.username,
                        points=player.rank_points
                    )
                )
            scoreboard = "\n".join(lines)

            embed = discord.Embed(
                title=t(guild_id, "top10.embed.title"),
                description=scoreboard,
                color=discord.Color.blue()
            )

            if myRank:
                embed.set_footer(text=t(guild_id, "top10.footer.my_rank", rank=myRank))
            else:
                embed.set_footer(text=t(guild_id, "top10.footer.no_rank"))

            await interaction.followup.send(embed=embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý /top10:", e)
            await interaction.followup.send(t(guild_id, "top10.error"))


async def setup(bot):
    await bot.add_cog(Top10(bot))
