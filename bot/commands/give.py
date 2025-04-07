import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository

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

        # Số tiền chuyển phải > 0
        if amount <= 0:
            await interaction.followup.send("⚠️ Số tiền chuyển phải lớn hơn 0.")
            return

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                sender = playerRepo.getById(sender_id)
                receiver = playerRepo.getById(receiver_id)

                if sender is None:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                if receiver is None:
                    await interaction.followup.send("⚠️ Người nhận chưa đăng ký tài khoản.")
                    return

                if sender.coin_balance < amount:
                    await interaction.followup.send("⚠️ Số tiền chuyển vượt quá số dư của bạn.")
                    return

                # Thực hiện chuyển tiền
                sender.coin_balance -= amount
                receiver.coin_balance += amount

                session.commit()
                await interaction.followup.send(
                    f"✅ Bạn đã chuyển **{amount:,} Ryo** cho {target.mention}."
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý give:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Give(bot))
