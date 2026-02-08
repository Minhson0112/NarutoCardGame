import discord
from discord.ext import commands
from discord import app_commands
import traceback

from bot.config.database import getDbSession
from bot.repository.guildLanguageSettingRepository import GuildLanguageSettingRepository
from bot.services.guildLanguageCache import guildLanguageCache
from bot.services.i18n import t


class SetLanguage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="setlanguage",
        description="Thiết lập ngôn ngữ cho server"
    )
    @app_commands.describe(language="Ngôn ngữ")
    @app_commands.choices(
        language=[
            app_commands.Choice(name="Tiếng Việt", value="vi"),
            app_commands.Choice(name="English", value="en"),
        ]
    )
    async def setlanguage(
        self,
        interaction: discord.Interaction,
        language: app_commands.Choice[str]
    ):
        # guild-only
        if interaction.guild is None:
            await interaction.response.send_message(
                t(None, "setlanguage.server_only"),
                ephemeral=True
            )
            return

        guild_id = interaction.guild.id

        # admin-only
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                t(guild_id, "setlanguage.admin_only"),
                ephemeral=True
            )
            return

        await interaction.response.defer(thinking=True)

        try:
            with getDbSession() as session:
                repo = GuildLanguageSettingRepository(session)
                setting = repo.upsertLanguage(
                    guildId=guild_id,
                    languageCode=language.value
                )

                # update cache immediately
                guildLanguageCache.setLanguage(guild_id, setting.language_code)

            # use the NEW language after setting
            await interaction.followup.send(
                t(guild_id, "setlanguage.success", language=setting.language_code)
            )

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(
                t(guild_id, "setlanguage.error", trace=tb),
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(SetLanguage(bot))
