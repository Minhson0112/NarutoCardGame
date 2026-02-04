import discord
from discord.ext import commands
from discord import app_commands

from bot.services.i18n import t


class HelpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Help")
    async def help(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id if interaction.guild else None

        community_link = "https://discord.gg/VxrMc2sBFP"

        embed_overview = discord.Embed(
            title=t(guild_id, "help.embed.overview.title"),
            color=discord.Color.blue(),
            description=t(guild_id, "help.embed.overview.desc"),
        )

        embed_start = discord.Embed(
            title=t(guild_id, "help.embed.start.title"),
            color=discord.Color.green(),
            description=t(guild_id, "help.embed.start.desc"),
        )

        embed_earn = discord.Embed(
            title=t(guild_id, "help.embed.earn.title"),
            color=discord.Color.gold(),
            description=t(guild_id, "help.embed.earn.desc"),
        )

        embed_interact = discord.Embed(
            title=t(guild_id, "help.embed.interact.title"),
            color=discord.Color.purple(),
            description=t(guild_id, "help.embed.interact.desc"),
        )

        embed_community = discord.Embed(
            title=t(guild_id, "help.embed.community.title"),
            color=discord.Color.teal(),
            description=t(guild_id, "help.embed.community.desc", community_link=community_link),
        )

        embeds = [embed_overview, embed_start, embed_earn, embed_interact, embed_community]
        await interaction.response.send_message(embeds=embeds)


async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCommand(bot))
