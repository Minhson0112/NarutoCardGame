import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.repository.gachaPityCounterRepository import GachaPityCounterRepository
from bot.services.playerService import PlayerService
from bot.services.i18n import t


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="register", description="Đăng ký tài khoản Naruto Card Game")
    async def register(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        guild_id = interaction.guild.id if interaction.guild else None
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
                    await interaction.followup.send(t(guild_id, "register.success"))
                else:
                    await interaction.followup.send(t(guild_id, "register.already_registered"))

        except Exception as e:
            print("❌ Lỗi khi đăng ký:", e)
            await interaction.followup.send(t(guild_id, "register.error"))


async def setup(bot):
    await bot.add_cog(Register(bot))
