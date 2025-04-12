import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Hiển thị danh sách các lệnh của bot")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Danh sách các lệnh của Bot",
            color=discord.Color.blue(),
            description="Dưới đây là danh sách các lệnh của bot được chia theo nhóm:"
        )

        embed.add_field(
            name="Lệnh cá nhân",
            value=(
                "/register\n"
                "/checkmoney\n"
                "/showprofile\n"
                "/give\n"
                "/inventory\n"
                "/rename\n"
                "/top10"
            ),
            inline=False
        )

        embed.add_field(
            name="Lệnh nội dung game chính",
            value=(
                "/showcard\n"
                "/shopweapon\n"
                "/buyCard\n"
                "/buyweapon\n"
                "/setcard\n"
                "/setweapon\n"
                "/levelupcad\n"
                "/levelupweapon\n"
                "/sellcard\n"
                "/sellweapon\n"
                "/fight\n"
                "/fightwith\n"
                "/challenge"
            ),
            inline=False
        )

        embed.add_field(
            name="Lệnh minigame",
            value=(
                "/slot\n"
                "/blackjack\n"
                "/coinflip\n"
                "/bingo"
            ),
            inline=False
        )

        embed.add_field(
            name="Các lệnh khác",
            value=(
                "/gifcode\n"
                "/devinfo"
            ),
            inline=False
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCommand(bot))
