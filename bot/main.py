import discord
from discord.ext import commands, tasks
import asyncio
from bot.config.config import DISCORD_TOKEN
<<<<<<< HEAD
=======
from bot.services.guildLanguageCache import guildLanguageCache
from bot.config.init_db import init_db
>>>>>>> a810d81 (cập nhập chợ đen và thuế)

# Định nghĩa intents – bắt buộc nếu muốn bot đọc tin nhắn hoặc phản hồi người dùng
intents = discord.Intents.default()
intents.message_content = True  # Cho phép đọc nội dung tin nhắn (bật trong Discord Dev Portal nữa)
intents.guilds = True  # BẮT BUỘC để đếm số server

# Tạo bot instance với prefix "/"
bot = commands.Bot(command_prefix="/", intents=intents)

# TASK LOOP cập nhật status
@tasks.loop(minutes=10)
async def update_status():
    guild_count = len(bot.guilds)
    await bot.change_presence(
        activity=discord.Game(name=f"trong {guild_count} server | /help")
    )


# Sự kiện khi bot sẵn sàng
@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔧 Slash commands đã sync: {len(synced)} lệnh")
    except Exception as e:
        print(f"❌ Lỗi sync commands: {e}")

    update_status.start()


# Hàm main để load các extension
async def main():
    # Khởi tạo DB tự động (tạo bảng nếu chưa có)
    init_db()

    # Danh sách các module cần load
    extensions = [
        "bot.commands.register",
        "bot.commands.daily",
        "bot.commands.checkMoney",
        "bot.commands.buyCard",
        "bot.commands.buyWeapon",
        "bot.commands.inventory",
        "bot.commands.showProfile",
        "bot.commands.setCard",
        "bot.commands.setWeapon",
        "bot.commands.levelupCard",
        "bot.commands.levelupWeapon",
        "bot.commands.give",
        "bot.commands.giveawayryo",
        "bot.commands.sellcard",
        "bot.commands.sellweapon",
        "bot.commands.fight",
        "bot.commands.fightWith",
        "bot.commands.bingo",
        "bot.commands.coinflip",
        "bot.commands.slot",
        "bot.commands.blackjack",
        "bot.commands.rename",
        "bot.commands.top10",
        "bot.commands.devinfo",
        "bot.commands.challenge",
        "bot.commands.giftcode",
        "bot.commands.help",
        "bot.commands.narutotrap",
        "bot.commands.dailyTask",
        "bot.commands.sellAllCard",
        "bot.commands.unequipweapon",
        "bot.commands.battlerule",
        "bot.commands.adventure",
        "bot.commands.tailedboss",
        "bot.commands.resetrank",
        "bot.commands.showcard",
        "bot.commands.lockcard",
        "bot.commands.unlockcard",
        "bot.commands.showweapon",
        "bot.commands.buyMultiCard",
        "bot.commands.shop",
<<<<<<< HEAD
=======
        "bot.commands.setLanguage",
        "bot.commands.market",
>>>>>>> a810d81 (cập nhập chợ đen và thuế)
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
