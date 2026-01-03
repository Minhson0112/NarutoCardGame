import discord
from discord.ext import commands
from discord import app_commands
import random
from datetime import date

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.gifcodeRepository import GifcodeRepository
from bot.repository.gifcodeLogRepository import GifcodeLogRepository

class GiftcodeGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="giftcode", description="Sử dụng mã GIFT để nhận quà")
    @app_commands.describe(
        code="Mã GIFT bạn muốn sử dụng"
    )
    async def giftcode(self, interaction: discord.Interaction, code: str):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                # Khởi tạo repository cần thiết
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                gifcodeRepo = GifcodeRepository(session)
                gifcodeLogRepo = GifcodeLogRepository(session)
                playerCardRepo = PlayerCardRepository(session)
                playerWeaponRepo = PlayerWeaponRepository(session)

                # Kiểm tra mã GIF có tồn tại không
                gifcodeEntry = gifcodeRepo.getByGifCode(code)
                if not gifcodeEntry:
                    await interaction.followup.send("⚠️ Mã GIFT không tồn tại. Vui lòng kiểm tra lại.")
                    return

                # Kiểm tra hạn sử dụng nếu có
                if gifcodeEntry.expiration_date is not None:
                    if date.today() > gifcodeEntry.expiration_date:
                        await interaction.followup.send("⚠️ Mã GIFT này đã hết hạn sử dụng.")
                        return

                # Kiểm tra xem người chơi đã dùng mã này chưa
                if gifcodeLogRepo.hasPlayerUsed(player_id, gifcodeEntry.id):
                    await interaction.followup.send("⚠️ Bạn đã sử dụng mã GIFT này trước đó và không thể sử dụng lại.")
                    return

                # Xử lý quà tặng dựa vào các cột của gifcodeEntry:
                rewards = []  # để lưu thông tin quà tặng đã nhận

                if gifcodeEntry.bonus_ryo is not None:
                    player.coin_balance += gifcodeEntry.bonus_ryo 
                    rewards.append(f"Bonus Ryo: {gifcodeEntry.bonus_ryo} Ryo")

                if gifcodeEntry.card_key is not None:
                    # Thêm thẻ vào kho của người chơi
                    playerCardRepo.incrementQuantity(player_id, gifcodeEntry.card_key, increment=1)
                    # Lấy tên thẻ từ quan hệ cardTemplate nếu có, ngược lại dùng gif_name như dự phòng
                    cardName = (gifcodeEntry.cardTemplate.name 
                                if gifcodeEntry.cardTemplate and gifcodeEntry.cardTemplate.name 
                                else gifcodeEntry.gif_name)
                    rewards.append(f"Thẻ: {cardName}")

                if gifcodeEntry.weapon_key is not None:
                    # Thêm vũ khí vào kho của người chơi
                    playerWeaponRepo.incrementQuantity(player_id, gifcodeEntry.weapon_key, increment=1)
                    # Lấy tên vũ khí từ quan hệ weaponTemplate nếu có, ngược lại dùng thông báo mặc định
                    weaponName = (gifcodeEntry.weaponTemplate.name 
                                if gifcodeEntry.weaponTemplate and gifcodeEntry.weaponTemplate.name 
                                else "Vũ khí")
                    rewards.append(f"Vũ khí: {weaponName}")

                # Ghi log lại việc sử dụng mã GIF (đặt ngoài khối if để luôn thực hiện)
                gifcodeLogRepo.createGifcodeLog(player_id, gifcodeEntry.id)

                session.commit()

                reward_str = ", ".join(rewards) if rewards else "Không có phần thưởng nào."
                response = (
                    f"✅ Bạn đã sử dụng thành công mã GIFT!\n"
                    f"Phần quà nhận được: {reward_str}\n"
                )
                await interaction.followup.send(response)
        except Exception as e:
            print("❌ Lỗi khi xử lý /gifcode:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(GiftcodeGame(bot))
