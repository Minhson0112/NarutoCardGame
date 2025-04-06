import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository

class CheckMoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="checkmoney", description="Kiểm tra số dư Ryo hiện tại của bạn")
    async def checkMoney(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(playerId)

                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!")
                    return

                coin = player.coin_balance
                await interaction.followup.send(f"💰 Số dư hiện tại của bạn là **{coin:,} Ryo**")
        except Exception as e:
            print("❌ Lỗi khi xử lý checkmoney:", e)
            await interaction.followup.send("❌ Đã xảy ra lỗi. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(CheckMoney(bot))
