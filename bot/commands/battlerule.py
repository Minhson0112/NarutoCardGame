import discord
from discord.ext import commands
from discord import app_commands

class BattleRule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="battlerule",
        description="Hiển thị luật battle và thông tin skill đặc biệt"
    )
    async def battlerule(self, interaction: discord.Interaction):
        # Embed 1: Luật battle
        embed1 = discord.Embed(
            title="📜 Luật Battle",
            color=discord.Color.blue()
        )
        embed1.description = (
            "🔹 **Mỗi đội** có 3 thẻ (Tanker, Middle, Back) (đã tích hợp sẵn vũ khí nếu lắp)\n"
            "🏎️ Team nào có tổng **Tốc độ** lớn hơn sẽ được quyền đánh **trước**\n"
            "🎯 Đòn tấn công cơ bản ưu tiên mục tiêu: **Tanker → Middle → Back**\n"
            "💧 Nếu **Chakra** của thẻ lên **100**, lượt kế nó sẽ dùng **Skill Đặc Biệt**\n"
            "💧 **Chakra** của thẻ sẽ tăng 20 sau mỗi lần ra đòn hoặc kết liễu tướng đối phương, tăng khi nhận sát thương theo % máu tối đa bị mất\n"
            "💀 Trận đấu kết thúc khi một bên có cả **3 thẻ đều chết**\n"
            "⏳ Nếu quá **120 lượt** mà chưa phân thắng bại thì **hòa**\n"
            "⚔️ Xem kĩ năng đặc biệt tướng bằng lệnh `/showcard`"
        )

        
        await interaction.response.send_message(embed=embed1)
        
async def setup(bot):
    await bot.add_cog(BattleRule(bot))
