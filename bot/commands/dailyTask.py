import discord
from discord.ext import commands
from discord import app_commands
from datetime import date

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.config.dailyTask import DAILY_TASK_CONFIG  # Chứa requirement & reward cho các nhiệm vụ hằng ngày

class DailyTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Mô tả chi tiết cho từng nhiệm vụ
        self.taskDescriptions = {
            "fight_win": "Thắng 10 lần bằng lệnh `/fight`",
            "minigame": "Chơi 10 lần minigame với bot",
            "fightwith": "Khiêu chiến 5 lần với bạn bè bằng `/fightwith`",
            "shop_buy": "Mua đồ trong shop 3 lần",
            "shop_sell": "Bán đồ cho shop 3 lần",
            "stage_clear": "Chiến thắng ải ít nhất 1 lần bằng lệnh `/challenge`",
        }
        
        # Emoji cho từng nhiệm vụ
        self.taskEmojis = {
            "fight_win": "⚔️",
            "minigame": "🎮",
            "fightwith": "🤼",
            "shop_buy": "🛍️",
            "shop_sell": "💸",
            "stage_clear": "🏆",
        }

    @app_commands.command(
        name="dailytask",
        description="Kiểm tra tiến độ nhiệm vụ hằng ngày và nhận thưởng"
    )
    async def dailytask(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id
        
        try:
            with getDbSession() as session:
                # Lấy thông tin người chơi
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return
                
                # Lấy thông tin nhiệm vụ hằng ngày của người chơi (sẽ tự động reset nếu ngày không khớp)
                dailyTaskRepo = DailyTaskRepository(session)
                dailyTask = dailyTaskRepo.getDailyTaskInfo(playerId)
                
                # Lấy tiến độ của từng nhiệm vụ từ bảng daily_tasks
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
                for taskKey, currentCount in tasksProgress.items():
                    requirement = DAILY_TASK_CONFIG[taskKey]["requirement"]
                    reward = DAILY_TASK_CONFIG[taskKey]["reward"]
                    fullDesc = self.taskDescriptions.get(taskKey, taskKey)
                    emoji = self.taskEmojis.get(taskKey, "")
                    
                    # Nếu đã hoàn thành nhiệm vụ, cộng thưởng và reset bộ đếm của nhiệm vụ đó
                    if currentCount >= requirement:
                        totalReward += reward
                    
                    # Xây dựng chuỗi mô tả cho nhiệm vụ:
                    # Dòng 1: Bullet kèm emoji, mô tả nhiệm vụ và tiến độ
                    # Dòng 2: Thụt đầu dòng hiển thị phần thưởng (dùng emoji)
                    taskLine = f"{emoji} {fullDesc} (**{currentCount}/{requirement}**)\n"
                    rewardLine = f"• 💰 Thưởng: {reward:,} Ryo"
                    # Tạo khoảng cách 2 dòng giữa các nhiệm vụ
                    descriptionLines.append(f"{taskLine}{rewardLine}\n")

                # Cộng phần thưởng nếu có nhiệm vụ được hoàn thành
                if totalReward > 0:
                    player.coin_balance += totalReward
                
                session.commit()
                
                embed = discord.Embed(
                    title=f"Nhiệm vụ hằng ngày của {player.username}",
                    color=discord.Color.green()
                )
                # Nối các chuỗi, mỗi nhiệm vụ cách nhau hai dòng
                embed.description = "\n\n".join(descriptionLines)
                
                if totalReward > 0:
                    embed.add_field(
                        name="Phần thưởng",
                        value=f"Bạn đã nhận tổng {totalReward:,} Ryo! từ nhiệm vụ hôm nay.",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name="Chưa đạt thưởng",
                        value="Hãy nỗ lực hoàn thành các nhiệm vụ để nhận thưởng.",
                        inline=False
                    )
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            print("❌ Lỗi khi xử lý dailytask:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra khi kiểm tra nhiệm vụ hằng ngày. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(DailyTask(bot))
