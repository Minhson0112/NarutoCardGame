import discord
from discord.ext import commands
from discord import app_commands

from bot.services.i18n import t


class DevInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.developerName = "Soun"
        self.authorName = "Son Kakashi"
        self.contactUrl = "https://www.facebook.com/son.developer2k"
        self.iconUrl = "https://i.imgur.com/example.png"

    @app_commands.command(
        name="devinfo",
        description="Hiển thị thông tin nhà phát triển"
    )
    async def devinfo(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id if interaction.guild else None

        embed = discord.Embed(
            title=t(guild_id, "devinfo.embed.title"),
            description=t(
                guild_id,
                "devinfo.embed.description",
                developerName=self.developerName,
                contactUrl=self.contactUrl
            ),
            color=discord.Color.blue()
        )

        embed.set_author(
            name=t(guild_id, "devinfo.embed.author_name", authorName=self.authorName),
            url=self.contactUrl,
            icon_url=self.iconUrl
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(DevInfo(bot))
