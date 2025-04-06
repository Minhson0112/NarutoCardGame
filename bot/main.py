import discord
from discord.ext import commands
import asyncio
from bot.config.config import DISCORD_TOKEN

# Định nghĩa intents – bắt buộc nếu muốn bot đọc tin nhắn hoặc phản hồi người dùng
intents = discord.Intents.default()
intents.message_content = True  # Cho phép đọc nội dung tin nhắn (bật trong Discord Dev Portal nữa)

# Tạo bot instance với prefix "/"
bot = commands.Bot(command_prefix="/", intents=intents)

# Sự kiện khi bot sẵn sàng
@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔧 Slash commands đã sync: {len(synced)} lệnh")
    except Exception as e:
        print(f"❌ Lỗi sync commands: {e}")

# Hàm main để load các extension
async def main():
    # Danh sách các module cần load
    extensions = [
        "bot.commands.register",
        "bot.commands.daily",
        "bot.commands.checkMoney",
        "bot.commands.shopCard",
        "bot.commands.shopWeapon",
        "bot.commands.buyCard",
        "bot.commands.buyWeapon",
        "bot.commands.inventory",
        "bot.commands.showProfile",
        "bot.commands.setCard",
        "bot.commands.setWeapon",
        "bot.commands.levelupCard",
        "bot.commands.levelupWeapon",
    ]

    # Load từng extension
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Đã load {ext}")
        except Exception as e:
            print(f"❌ Không thể load {ext}: {e}")

    # Bắt đầu bot
    await bot.start(DISCORD_TOKEN)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
