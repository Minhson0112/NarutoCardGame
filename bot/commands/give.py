import discord
from discord.ext import commands
from discord import app_commands
from datetime import date, datetime

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.config.config import LEVEL_RECEIVED_LIMIT, LEVEL_CONFIG

class Give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="give", description="Chuyển tiền cho người khác")
    @app_commands.describe(
        target="Tag của người nhận",
        amount="Số Ryo cần chuyển"
    )
    async def give(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        await interaction.response.defer(thinking=True)
        sender_id = interaction.user.id
        receiver_id = target.id

        if amount <= 0:
            await interaction.followup.send("⚠️ Số tiền chuyển phải lớn hơn 0.")
            return

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                sender = playerRepo.getById(sender_id)
                receiver = playerRepo.getById(receiver_id)

                # Kiểm tra tài khoản
                if sender is None:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return
                if receiver is None:
                    await interaction.followup.send("⚠️ Người nhận chưa đăng ký tài khoản.")
                    return
                if sender.coin_balance < amount:
                    await interaction.followup.send("⚠️ Số tiền chuyển vượt quá số dư của bạn.")
                    return

                # --- XỬ LÝ DAILY LIMIT ---
                today = date.today()
                # reset nếu ngày khác
                if receiver.daily_received_date.date() != today:
                    receiver.daily_received_amount = 0
                    receiver.daily_received_date = datetime.now()

                # Tính level của receiver từ exp
                exp = receiver.exp or 0
                # thresholds sorted, tìm level cao nhất mà exp >= threshold
                thresholds = sorted(int(k) for k in LEVEL_CONFIG.keys())
                level = 0
                for t in thresholds:
                    if exp >= t:
                        level = LEVEL_CONFIG[str(t)]
                    else:
                        break

                # Lấy limit cho level đó
                limit = LEVEL_RECEIVED_LIMIT.get(str(level), 0)

                # Nếu đã nhận + amount vượt limit → báo lỗi
                if receiver.daily_received_amount + amount > limit:
                    await interaction.followup.send(
                        f"⚠️ Người nhận đang ở cấp **{level}**, chỉ được nhận tối đa **{limit:,} Ryo** mỗi ngày.\n\n"
                        f"Hiện đã nhận **{receiver.daily_received_amount:,} Ryo** hôm nay."
                    )
                    return

                # --- Thực hiện chuyển tiền ---
                sender.coin_balance -= amount
                receiver.coin_balance += amount

                # Cộng vào daily_received_amount
                receiver.daily_received_amount += amount

                session.commit()

                await interaction.followup.send(
                    f"✅ Bạn đã chuyển **{amount:,} Ryo** cho {target.mention}."
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý give:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Give(bot))
