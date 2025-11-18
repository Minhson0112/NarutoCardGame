import discord
from discord.ext import commands
from discord import app_commands

class DevInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="devinfo", description="Hiển thị thông tin nhà phát triển")
    async def devinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🌟 Thông tin Nhà Phát Triển 🌟",
            description=(
                "Bot được phát triển bởi **Soun**.\n\n"
                "Nếu bạn gặp lỗi hoặc có góp ý, hãy nhấn vào [đây](https://www.facebook.com/son.developer2k) để liên hệ.\n\n"
                "Cảm ơn bạn đã sử dụng bot! ❤️"
            ),
            color=discord.Color.blue()
        )
        # Nếu muốn, có thể dùng trường Author để làm cho đường link hiển thị dưới tên của nhà phát triển:
        embed.set_author(name="Son Kakashi", url="https://www.facebook.com/son.developer2k", icon_url="https://i.imgur.com/example.png")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DevInfo(bot))
