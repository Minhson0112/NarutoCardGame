import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Hướng dẫn cho người mới bắt đầu sử dụng bot")
    async def help(self, interaction: discord.Interaction):
        # Embed Giới thiệu game
        embed_overview = discord.Embed(
            title="📜 Giới thiệu game",
            color=discord.Color.blue(),
            description=(
                "Game của chúng ta xoay quanh việc thu thập các thẻ nhân vật từ anime **Naruto** với độ hiếm khác nhau. \n"
                "Bạn sẽ sử dụng các thẻ này để **PK** với nhau, tham gia đánh ải cốt truyện, leo bảng xếp hạng và trải nghiệm nhiều trò chơi thú vị khác."
            )
        )

        # Embed Hướng dẫn bắt đầu
        embed_start = discord.Embed(
            title="🚀 Xuất phát nào",
            color=discord.Color.green(),
            description=(
                "• Tạo tài khoản ngay bằng lệnh ``/register`` để bắt đầu hành trình của bạn."
            )
        )

        # Embed Hướng dẫn kiếm tiền
        embed_earn = discord.Embed(
            title="💰 Cách kiếm tiền",
            color=discord.Color.gold(),
            description=(
                "1. Điểm danh mỗi ngày bằng lệnh ``/daily`` để nhận tiền điểm danh.\n\n"
                "2. Hoàn thành các nhiệm vụ hằng ngày bằng lệnh ``/dailytask`` để nhận thưởng.\n\n"
                "3. Tham gia đánh ải cốt truyện bằng lệnh ``/challenge`` – càng đánh càng được thưởng nhiều.\n\n"
                "4. Thử vận may với lệnh ``/fight`` để leo bảng xếp hạng; chuỗi thắng cao sẽ nhận thêm tiền.\n\n"
                "5. Chơi minigame với bot qua các lệnh ``/slot``, ``/blackjack``, ``/coinflip``, ``/bingo`` để kiếm tiền.\n\n"
                "6. Mua gói thẻ rẻ (với tỷ lệ rơi thẻ hiếm) và bán chúng bằng lệnh ``/sellcard`` hoặc ``/sellweapon`` để kiếm lời."
                "7. đi viễn chinh bằng ``/adventure ``, thắng sẽ nhận được tiền"
                "8. đánh boss vĩ thú bằng ``/tailedboss ``, nhận được tiền theo sát thương gây ra, hạ gục vĩ thú sẽ có tỉ lệ nhận được thẻ và vũ khí"
            )
        )

        # Embed Hướng dẫn tương tác với thẻ và vũ khí
        embed_interact = discord.Embed(
            title="🃏 Cách tương tác với thẻ và vũ khí",
            color=discord.Color.purple(),
            description=(
                "1. Ghé shop thẻ bằng lệnh ``/shopcard`` để xem các gói thẻ, tỷ lệ rơi và cách mua, cũng như số lần cần mua để đảm bảo nhận được thẻ hiếm (được cá nhân hóa cho từng người chơi).\n\n"
                "2. Sau khi mua, kiểm tra kho của bạn bằng lệnh ``/inventory``.\n\n"
                "3. Tương tự, bạn có thể vào shop vũ khí để mua vũ khí qua các lệnh tương tự.\n\n"
                "4. Nâng cấp thẻ và vũ khí bằng lệnh ``/levelupcard`` và ``/levelupweapon`` (nâng cấp sẽ tăng sức mạnh nếu bạn có các thẻ hoặc vũ khí giống nhau).\n\n"
                "5. Lắp thẻ mạnh nhất và vũ khí mạnh nhất vào hồ sơ của bạn bằng lệnh ``/setcard`` và ``/setweapon`` để chuẩn bị chiến đấu với các người chơi khác."
            )
        )

        # Embed Thông tin máy chủ cộng đồng
        embed_community = discord.Embed(
            title="🌐 Máy chủ cộng đồng",
            color=discord.Color.teal(),
            description=(
                "• Tham gia [máy chủ cộng đồng](https://discord.gg/Tbm2xuA2) của chúng ta để nhận thông báo về **gifcode** và các event hấp dẫn của bot.\n\n"
            )
        )

        # Gửi tất cả các embed cùng 1 lúc
        embeds = [embed_overview, embed_start, embed_earn, embed_interact, embed_community]
        await interaction.response.send_message(embeds=embeds)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCommand(bot))
