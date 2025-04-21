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
            "💀 Trận đấu kết thúc khi một bên có cả **3 thẻ đều chết**\n"
            "⏳ Nếu quá **120 lượt** mà chưa phân thắng bại thì **hòa**"
        )

        # Embed 2: Thông tin skill đặc biệt
        embed2 = discord.Embed(
            title="✨ Thông tin Skill Đặc Biệt",
            color=discord.Color.purple()
        )
        embed2.add_field(
            name="💧 Hệ Thủy (thuần buff)",
            value=(
                "**Genin**: Hồi máu 1 đồng minh thấp nhất bằng 600% SMKK\n"
                "**Chunin**: Hồi máu 2 đồng minh thấp nhất bằng 600% SMKK\n"
                "**Jounin**: Hồi máu 2 đồng minh thấp nhất 600% SMKK & buff Giáp +10% SMKK\n"
                "**Kage**: Hồi máu toàn đội 600% SMKK & buff Giáp +10% SMKK\n"
                "**Legendary**: Hồi máu toàn đội 600% SMKK, buff Giáp +10% SMKK & buff SMKK +30%"
            ),
            inline=False
        )
        embed2.add_field(
            name="🌍 Hệ Thổ (phá rối địch)",
            value=(
                "**Genin**: tấn công toàn đội địch & Giảm 15% SMKK\n"
                "**Chunin**: Như Genin + Giảm 50% Crit rate địch\n"
                "**Jounin**: Như Chunin + Giảm 15% né địch\n"
                "**Kage**: Như Jounin + Giảm 20 Chakra địch\n"
                "**Legendary**: Như Kage + Gây 200% sát thương lên toàn địch"
            ),
            inline=False
        )
        embed2.add_field(
            name="🌪️ Hệ Phong (sát thương mạnh, kết liễu)",
            value=(
                "**Genin**: Gây 300% sát thương toàn địch, giảm 20% mỗi địch trúng chiêu, ngay lập tức kết liễu địch <5% máu\n"
                "**Chunin**: Như Genin, mốc <10% máu\n"
                "**Jounin**: Như Genin, mốc <15% máu\n"
                "**Kage**: Như Genin, mốc <20% máu\n"
                "**Legendary**: Như Genin, mốc <25% máu"
            ),
            inline=False
        )
        embed2.add_field(
            name="⚡ Hệ Lôi (nhanh và né)",
            value=(
                "**Genin**: Gây 400% sát thương lên kẻ địch đầu tiên, +5% né bản thân\n"
                "**Chunin**: Như Genin +10% né bản thân\n"
                "**Jounin**: Gây 400% sát thương lên 2 kẻ địch đầu tiên +15% né bản thân\n"
                "**Kage**:  Gây 400% sát thương lên toàn bộ kẻ địch +20% né bản thân\n"
                "**Legendary**: Như Kage, +20% né toàn bộ đồng minh"
            ),
            inline=False
        )
        embed2.add_field(
            name="🔥 Hệ Hỏa (giảm hồi phục, phá giáp, sát thương chuẩn)",
            value=(
                "**Genin**: Gây 300% sát thương lên địch đầu tiên, giảm hồi phục 15%\n"
                "**Chunin**: Như Genin cho 2 địch đầu, giảm hồi phục 20%\n"
                "**Jounin**: 300% toàn địch, giảm hồi phục 25%\n"
                "**Kage**: 300% sát thương chuẩn (bỏ qua giáp), giảm hồi phục 25%\n"
                "**Legendary**: Như Kage + Giảm giáp địch 30%"
            ),
            inline=False
        )
        embed2.add_field(
            name="🏋️‍♂️ Hệ Thể (thể thuật)",
            value=(
                "**Genin**: Tăng 150% toàn bộ chỉ số bản thân & hồi 30% máu đã mất\n"
                "**Chunin**: Tăng 180% & hồi 30%\n"
                "**Jounin**: Tăng 220% & hồi 30%\n"
                "**Kage**: Tăng 250% & hồi 30%\n"
                "**Legendary**: Tăng 300% & hồi 30%"
            ),
            inline=False
        )

        await interaction.response.send_message(embeds=[embed1, embed2])
        

async def setup(bot):
    await bot.add_cog(BattleRule(bot))
