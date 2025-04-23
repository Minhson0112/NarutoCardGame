import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository

class Slot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Danh sách các emoji cho máy slot – bạn có thể mở rộng thêm theo mong muốn
        self.slot_emojis = ["🍒", "🍋", "🍊", "🍇", "🍉", "⭐", "💎"]

    @app_commands.command(name="slot", description="Chơi máy slot để trúng thưởng 🎰")
    @app_commands.describe(bet="Số tiền cược bạn muốn đặt (Ryo)")
    async def slot(self, interaction: discord.Interaction, bet: int):
        # Tạm hoãn phản hồi ban đầu để xử lý logic lâu hơn
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                # Kiểm tra thông tin người chơi và số dư
                playerRepo = PlayerRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return
                if bet <= 0:
                    await interaction.followup.send("⚠️ Số tiền cược phải lớn hơn 0.")
                    return
                if bet > 1000000:
                    await interaction.followup.send("⚠️ Số tiền cược không được quá 1m.")
                    return
                if player.coin_balance < bet:
                    await interaction.followup.send("⚠️ Số dư của bạn không đủ.")
                    return
                
                dailyTaskRepo.updateMinigame(player_id)
                # Random ra 3 emoji (3 ngăn quay)
                outcome = [random.choice(self.slot_emojis) for _ in range(3)]
                unique_count = len(set(outcome))
                if unique_count == 1:
                    multiplier = 10
                elif unique_count == 2:
                    multiplier = 2
                else:
                    multiplier = 0

                # Gửi thông báo ban đầu
                initial_embed = discord.Embed(
                    title="🎰 Máy Slot 🎰",
                    description=f"💰 Tiền cược: **{bet} Ryo**\n🎮 Đang quay thưởng...",
                    color=discord.Color.gold()
                )
                msg = await interaction.followup.send(embed=initial_embed)

                # Cập nhật 1: Hiển thị emoji thứ nhất
                await asyncio.sleep(0.5)
                embed_step1 = discord.Embed(
                    title="🎰 Máy Slot 🎰",
                    description=f"{outcome[0]}",
                    color=discord.Color.gold()
                )
                await msg.edit(embed=embed_step1)

                # Cập nhật 2: Hiển thị emoji thứ nhất và thứ hai
                await asyncio.sleep(0.5)
                embed_step2 = discord.Embed(
                    title="🎰 Máy Slot 🎰",
                    description=f"{outcome[0]} | {outcome[1]}",
                    color=discord.Color.gold()
                )
                await msg.edit(embed=embed_step2)

                # Cập nhật 3: Hiển thị đủ 3 emoji
                await asyncio.sleep(0.5)
                embed_step3 = discord.Embed(
                    title="🎰 Máy Slot 🎰",
                    description=f"{outcome[0]} | {outcome[1]} | {outcome[2]}",
                    color=discord.Color.gold()
                )
                await msg.edit(embed=embed_step3)

                # Chờ thêm một chút để đảm bảo người dùng có thể theo dõi quá trình hiển thị
                await asyncio.sleep(1)

                # Xử lý kết quả và cập nhật số dư của người chơi
                if multiplier > 0:
                    reward = bet * multiplier
                    if multiplier == 10:
                        outcome_text = (
                            f"🥳 Chúc mừng! Máy Slot ra: **{' | '.join(outcome)}**.\n"
                            f"Bạn trúng jackpot, nhận thưởng **{reward} Ryo** (Cược x10)."
                        )
                    else:
                        outcome_text = (
                            f"😊 Chúc mừng! Máy Slot ra: **{' | '.join(outcome)}**.\n"
                            f"Bạn trúng thưởng, nhận thưởng **{reward} Ryo** (Cược x2)."
                        )
                    player.coin_balance = player.coin_balance - bet + reward
                    final_color = discord.Color.green()
                else:
                    outcome_text = (
                        f"😢 Rất tiếc! Máy Slot ra: **{' | '.join(outcome)}**.\n"
                        f"Bạn thất bại, mất hết số tiền cược (**{bet} Ryo**)."
                    )
                    player.coin_balance -= bet
                    final_color = discord.Color.red()
                
                session.commit()

                # Cập nhật cuối cùng: Hiển thị kết quả đầy đủ
                final_embed = discord.Embed(
                    title="🎰 Kết quả Máy Slot 🎰",
                    description=(
                        f"**Kết quả quay:** {' | '.join(outcome)}\n\n"
                        f"{outcome_text}\n\n"
                        f"💰 Số dư hiện tại: **{player.coin_balance} Ryo**"
                    ),
                    color=final_color
                )
                await msg.edit(embed=final_embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý /slot:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Slot(bot))
