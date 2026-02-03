import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.config.dailyTask import DAILY_TASK_CONFIG
from bot.services.i18n import t


class DailyTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.taskEmojis = {
            "fight_win": "⚔️",
            "minigame": "🎮",
            "fightwith": "🤼",
            "shop_buy": "🛍️",
            "shop_sell": "💸",
            "stage_clear": "🏆",
        }

        self.taskKeys = [
            "fight_win",
            "minigame",
            "fightwith",
            "shop_buy",
            "shop_sell",
            "stage_clear",
        ]

    @app_commands.command(
        name="dailytask",
        description="Kiểm tra tiến độ nhiệm vụ hằng ngày và nhận thưởng"
    )
    async def dailytask(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        guild_id = interaction.guild.id if interaction.guild else None
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(t(guild_id, "dailytask.not_registered"))
                    return

                dailyTaskRepo = DailyTaskRepository(session)
                dailyTask = dailyTaskRepo.getDailyTaskInfo(player_id)

                tasksProgress = {
                    "fight_win": dailyTask.fight_win_count,
                    "minigame": dailyTask.minigame_count,
                    "fightwith": dailyTask.fightwith_count,
                    "shop_buy": dailyTask.shop_buy_count,
                    "shop_sell": dailyTask.shop_sell_count,
                    "stage_clear": dailyTask.stage_clear_count,
                }

                totalReward = 0
                descriptionLines = []

                for taskKey in self.taskKeys:
                    currentCount = tasksProgress.get(taskKey, 0)
                    requirement = DAILY_TASK_CONFIG[taskKey]["requirement"]
                    reward = DAILY_TASK_CONFIG[taskKey]["reward"]

                    fullDesc = t(guild_id, f"dailytask.task.{taskKey}")
                    emoji = self.taskEmojis.get(taskKey, "")

                    claimed = getattr(dailyTask, f"{taskKey}_claimed")
                    if currentCount >= requirement:
                        if not claimed:
                            totalReward += reward
                            setattr(dailyTask, f"{taskKey}_claimed", True)
                        claim_status = t(guild_id, "dailytask.claimed")
                    else:
                        claim_status = t(guild_id, "dailytask.not_enough")

                    taskLine = f"{emoji} {fullDesc} (**{currentCount}/{requirement}**) - {claim_status}\n"
                    rewardLine = t(guild_id, "dailytask.reward_line", reward=reward)
                    descriptionLines.append(f"{taskLine}{rewardLine}\n")

                if totalReward > 0:
                    player.coin_balance += totalReward

                session.commit()

                embed = discord.Embed(
                    title=t(guild_id, "dailytask.title", username=player.username),
                    color=discord.Color.green()
                )
                embed.description = "\n\n".join(descriptionLines)

                if totalReward > 0:
                    embed.add_field(
                        name=t(guild_id, "dailytask.field_reward_name"),
                        value=t(guild_id, "dailytask.field_reward_value", totalReward=totalReward),
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=t(guild_id, "dailytask.field_info_name"),
                        value=t(guild_id, "dailytask.field_info_value"),
                        inline=False
                    )

                await interaction.followup.send(embed=embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý dailytask:", e)
            await interaction.followup.send(t(guild_id, "dailytask.error"))


async def setup(bot):
    await bot.add_cog(DailyTask(bot))
