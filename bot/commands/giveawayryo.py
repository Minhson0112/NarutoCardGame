import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.config.config import ADMIN_OVERRIDE_ID

class GiveawayRyo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="giveawayryo", description="Có vẻ bạn không có quyền dùng lệnh này: Tặng Ryo")
    @app_commands.describe(
        target="Tag của người nhận",
        amount="Số Ryo muốn tặng"
    )
    async def giveawayRyo(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        await interaction.response.defer(thinking=True)
        dev_id = interaction.user.id

        # Kiểm tra quyền admin dựa trên ADMIN_OVERRIDE_ID
        if dev_id not in ADMIN_OVERRIDE_ID:
            await interaction.followup.send("⚠️ Bạn không có quyền sử dụng lệnh này. Hãy dùng /give để chuyển tiền.")
            return

        if amount <= 0:
            await interaction.followup.send("⚠️ Số Ryo tặng phải lớn hơn 0.")
            return

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                receiver = playerRepo.getById(target.id)
                if not receiver:
                    await interaction.followup.send("⚠️ Người nhận chưa đăng ký tài khoản.")
                    return

                # Cộng số Ryo cho người nhận và commit
                receiver.coin_balance += amount
                session.commit()

                await interaction.followup.send(f"✅ Đã giveaway **{amount:,} Ryo** cho {target.mention}.")
        except Exception as e:
            print("❌ Lỗi khi xử lý giveawayryo:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(GiveawayRyo(bot))
