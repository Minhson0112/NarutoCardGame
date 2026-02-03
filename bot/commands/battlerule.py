import discord
from discord.ext import commands
from discord import app_commands
from bot.services.i18n import t

class BattleRule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="battlerule",
        description="Hiển thị luật battle và thông tin skill đặc biệt"
    )
    async def battlerule(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id if interaction.guild else None

        embed = discord.Embed(
            title=t(guild_id, "battlerule.title"),
            description=t(guild_id, "battlerule.desc"),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(BattleRule(bot))