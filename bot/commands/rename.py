import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.services.i18n import t


class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rename", description="Đổi tên của bạn (tối đa 16 ký tự)")
    @app_commands.describe(new_name="Tên mới của bạn (tối đa 16 ký tự)")
    async def rename(self, interaction: discord.Interaction, new_name: str):
        guild_id = interaction.guild.id if interaction.guild else None

        if len(new_name) > 16:
            await interaction.response.send_message(
                t(guild_id, "rename.too_long"),
                ephemeral=True
            )
            return

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(interaction.user.id)
                if not player:
                    await interaction.response.send_message(
                        t(guild_id, "rename.not_registered"),
                        ephemeral=True
                    )
                    return

                player.username = new_name
                session.commit()

                await interaction.response.send_message(
                    t(guild_id, "rename.success", newName=new_name),
                    ephemeral=True
                )

        except Exception as e:
            print("❌ Lỗi khi đổi tên:", e)
            await interaction.response.send_message(
                t(guild_id, "rename.error"),
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Rename(bot))
