import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.config.config import ADMIN_OVERRIDE_ID
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.entity.player import Player
from bot.services.i18n import t


class ResetRank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="resetrank",
        description="(Dev only) Reset điểm rank, chuỗi thắng và trao thưởng Top10"
    )
    async def resetrank(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id if interaction.guild else None

        if interaction.user.id not in ADMIN_OVERRIDE_ID:
            await interaction.response.send_message(
                t(guild_id, "resetrank.no_permission"),
                ephemeral=True
            )
            return

        await interaction.response.defer(thinking=True)
        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                playerCardRepo = PlayerCardRepository(session)

                topPlayers = playerRepo.getTop10()

                description_lines = []
                for idx, player in enumerate(topPlayers, start=1):
                    old_points = player.rank_points
                    award_value = (11 - idx) * 100_000
                    player.coin_balance += award_value

                    if award_value >= 1_000_000:
                        line = t(
                            guild_id,
                            "resetrank.top_line.million",
                            rank=idx,
                            username=player.username,
                            oldPoints=old_points
                        )
                    else:
                        reward_k = award_value // 1_000
                        line = t(
                            guild_id,
                            "resetrank.top_line.thousand",
                            rank=idx,
                            username=player.username,
                            oldPoints=old_points,
                            rewardK=reward_k
                        )

                    description_lines.append(line)

                session.query(Player).update(
                    {
                        Player.rank_points: 0,
                        Player.winning_streak: 0
                    },
                    synchronize_session=False
                )

                playerCardRepo.apply_rank_reset_level_penalty()
                session.commit()

            embed = discord.Embed(
                title=t(guild_id, "resetrank.announce.title"),
                description=(
                    "\n".join(description_lines)
                    + "\n\n"
                    + t(guild_id, "resetrank.announce.card_penalty")
                ),
                color=discord.Color.green()
            )
            embed.set_footer(text=t(guild_id, "resetrank.announce.footer"))
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý /resetrank:", e)
            await interaction.followup.send(t(guild_id, "resetrank.error"))


async def setup(bot):
    await bot.add_cog(ResetRank(bot))
