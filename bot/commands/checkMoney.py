import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.services.i18n import t


class CheckMoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="checkmoney", description="Kiểm tra số dư Ryo hiện tại của bạn")
    async def checkMoney(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        playerId = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(playerId)

                if not player:
                    await interaction.followup.send(t(guild_id, "checkmoney.not_registered"))
                    return

                await interaction.followup.send(
                    t(guild_id, "checkmoney.balance", coin=player.coin_balance)
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý checkmoney:", e)
            await interaction.followup.send(t(guild_id, "checkmoney.error"))


async def setup(bot):
    await bot.add_cog(CheckMoney(bot))
