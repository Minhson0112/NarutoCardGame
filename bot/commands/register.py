import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.repository.gachaPityCounterRepository import GachaPityCounterRepository
from bot.services.playerService import PlayerService

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="register", description="Đăng ký tài khoản Naruto Card Game")
    async def register(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        playerId = interaction.user.id
        username = interaction.user.display_name

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                setupRepo = PlayerActiveSetupRepository(session)
                gachaRepo = GachaPityCounterRepository(session)
                service = PlayerService(playerRepo, setupRepo, gachaRepo)

                success = service.registerPlayer(playerId, username)

                if success:
                    await interaction.followup.send("✅ Bạn đã đăng ký tài khoản thành công!, tiếp theo hãy dùng lệnh /help để biết cách dùng bot nhé.")
                else:
                    await interaction.followup.send("⚠️ Bạn đã đăng ký rồi.")
        except Exception as e:
            print("❌ Lỗi khi đăng ký:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra khi đăng ký. Vui lòng thử lại.")

# Bắt buộc để load bằng load_extension()
async def setup(bot):
    await bot.add_cog(Register(bot))
