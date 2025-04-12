import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository

class Bingo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Định nghĩa mapping từ số đến emoji
        self.emoji_map = {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣"
        }

    @app_commands.command(name="bingo", description="Chơi bingo để trúng thưởng 🎉")
    @app_commands.describe(
        bet="Số tiền cược bạn muốn đặt 💰"
    )
    async def bingo(self, interaction: discord.Interaction, bet: int):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                # Lấy thông tin người chơi
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return
                
                if bet <= 0:
                    await interaction.followup.send("⚠️ Số tiền cược phải lớn hơn 0.")
                    return

                if player.coin_balance < bet:
                    await interaction.followup.send("⚠️ Số dư của bạn không đủ.")
                    return

                # Random số may mắn
                win_number = random.randint(1, 5)

                # Gửi thông báo với 5 reaction emoji và thêm vài emoji trang trí
                description = (
                    f"🌟 **Bingo Time!** 🌟\n\n"
                    f"Chọn số may mắn từ **1️⃣** đến **5️⃣**!\n"
                    f"Cược: **{bet} Ryo**\n"
                    f"❗ Nếu chọn đúng ngay từ lần đầu: nhận **x4** 🎉\n"
                    f"❗ Nếu chọn đúng ở lần thứ 2: nhận **x2** 😄\n"
                    f"❗ Nếu không đúng sau 2 lần: mất hết số tiền cược 😢"
                )
                # Gửi tin nhắn ban đầu
                await interaction.followup.send(content=description)
                # Lấy tin nhắn vừa gửi để thêm reaction
                msg = await interaction.original_response()
                for i in range(1, 6):
                    await msg.add_reaction(self.emoji_map[i])

                attempt = 0
                correct = False
                chosen_multiplier = 0

                def check(reaction, user):
                    return (
                        user.id == player_id
                        and reaction.message.id == msg.id
                        and str(reaction.emoji) in self.emoji_map.values()
                    )

                # Cho phép tối đa 2 lần cố gắng
                while attempt < 2 and not correct:
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    except asyncio.TimeoutError:
                        break
                    # Nếu phản hồi đúng
                    if str(reaction.emoji) == self.emoji_map[win_number]:
                        correct = True
                        chosen_multiplier = 4 if attempt == 0 else 2
                    else:
                        # Nếu phản hồi sai, xoá toàn bộ reaction đó để người chơi không chọn lại
                        try:
                            await msg.clear_reaction(reaction.emoji)
                        except Exception:
                            pass
                        attempt += 1

                # Cập nhật số dư và xác định kết quả
                if correct:
                    reward = bet * chosen_multiplier
                    if attempt == 0:
                        outcome_text = (
                            f"🥳 Chúc mừng! Con số may mắn của bạn là {self.emoji_map[win_number]}.\n"
                            f"Bạn đã chọn đúng ngay từ lần đầu, nhận thưởng là **{reward} Ryo**! 🎉"
                        )
                    else:
                        outcome_text = (
                            f"😊 Chúc mừng! Con số may mắn của bạn là {self.emoji_map[win_number]}.\n"
                            f"Bạn đã chọn đúng ở lần thứ 2, nhận thưởng là **{reward} Ryo**! 👍"
                        )
                    # Cược được trừ ra rồi thưởng: mới = (coin_balance - bet + reward)
                    player.coin_balance = player.coin_balance - bet + reward
                else:
                    outcome_text = (
                        f"😢 Rất tiếc! Con số may mắn của bạn là {self.emoji_map[win_number]}.\n"
                        f"Bạn chọn sai. Bạn mất hết số tiền cược (**{bet} Ryo**)."
                    )
                    player.coin_balance -= bet

                session.commit()

                # Tạo embed kết quả với trang trí emoji
                embed_outcome = discord.Embed(
                    title="🎲 Kết quả Bingo 🎲",
                    description=(
                        f"Số may mắn: {self.emoji_map[win_number]}\n\n"
                        f"{outcome_text}\n\n"
                        f"💰 Số dư hiện tại: **{player.coin_balance} Ryo**"
                    ),
                    color=discord.Color.blue()
                )

                # Cập nhật tin nhắn gốc với kết quả (không gửi tin nhắn mới)
                await interaction.edit_original_response(embed=embed_outcome)

        except Exception as e:
            print("❌ Lỗi khi xử lý /bingo:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Bingo(bot))
