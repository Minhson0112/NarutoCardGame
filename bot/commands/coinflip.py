import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Chơi lật đồng xu để trúng thưởng (dự đoán úp hoặc ngửa)")
    @app_commands.describe(
        bet="Số tiền cược bạn muốn đặt",
        guess="Dự đoán của bạn: u:úp hoặc n:ngửa"
    )
    async def coinflip(self, interaction: discord.Interaction, bet: int, guess: str):
        await interaction.response.defer(thinking=True)
        guess = guess.lower().strip()
        # Chỉ chấp nhận hai dự đoán: "úp" và "ngửa"
        if guess not in ["u", "n"]:
            await interaction.followup.send("⚠️ Vui lòng nhập đúng dự đoán: **u** hoặc **n**.")
            return

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                player = playerRepo.getById(interaction.user.id)
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
                
                dailyTaskRepo.updateMinigame(interaction.user.id)
                # Thực hiện lật đồng xu (random từ "úp" đến "ngửa")
                coin_result = random.choice(["u", "n"])
                
                # Xác định kết quả và cập nhật số dư:
                if guess == coin_result:
                    # Nếu dự đoán đúng, nhân thưởng gấp 2 số tiền cược
                    multiplier = 2
                    reward = bet * multiplier
                    outcome_text = (f"🥳 Chúc mừng! Kết quả là **{coin_result.upper()}**.\n"
                                    f"Bạn đã dự đoán đúng và nhận thưởng **{reward} Ryo**!")
                    # Số dư mới = (coin_balance - bet + reward)
                    player.coin_balance = player.coin_balance - bet + reward
                else:
                    outcome_text = (f"😢 Rất tiếc! Kết quả là **{coin_result.upper()}**.\n"
                                    f"Bạn đã dự đoán sai và mất hết số tiền cược (**{bet} Ryo**).")
                    player.coin_balance -= bet

                session.commit()

                # Tạo embed hiển thị kết quả
                embed_outcome = discord.Embed(
                    title="Kết quả Lật Đồng Xu",
                    description=(
                        f"**Kết quả:** {coin_result.upper()}\n"
                        f"{outcome_text}\n\n"
                        f"💰 Số dư hiện tại: **{player.coin_balance} Ryo**"
                    ),
                    color=discord.Color.purple()
                )

                await interaction.followup.send(embed=embed_outcome)

        except Exception as e:
            print("❌ Lỗi khi xử lý /coinflip:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(CoinFlip(bot))
