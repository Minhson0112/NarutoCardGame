from bot.config.database import Base, engine
import time
import bot.entity.player
import bot.entity.guildLanguageSetting
import bot.entity.dailyClaimLog
import bot.entity.cardTemplate
import bot.entity.challenge
import bot.entity.commandCooldown
import bot.entity.dailyTask
import bot.entity.gachaPityCounter
import bot.entity.gifcode
import bot.entity.gifcodeLog
import bot.entity.pkBattle
import bot.entity.playerCards
import bot.entity.playerWeapon
import bot.entity.weaponTemplate
import bot.entity.PlayerActiveSetup
import bot.entity.marketListing

def init_db():
    print("⏳ Đang đợi MySQL khởi động và kết nối...")
    max_retries = 10
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Thử kết nối và tạo bảng
            Base.metadata.create_all(bind=engine)
            print("✅ Khởi tạo Database hoàn tất!")
            return
        except Exception as e:
            retry_count += 1
            print(f"⚠️ Chưa thể kết nối MySQL (Lần thử {retry_count}/{max_retries}). Đang đợi 5 giây...")
            time.sleep(5)
    
    print("❌ Lỗi: Không thể kết nối với MySQL sau nhiều lần thử.")
