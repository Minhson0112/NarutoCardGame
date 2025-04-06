import discord
from discord.ext import commands
from discord import app_commands
import random
from sqlalchemy import func

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.weaponTemplateRepository import WeaponTemplateRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.services.playerService import PlayerService
from bot.config.weaponGachaConfig import WEAPON_GACHA_PRICES, WEAPON_GACHA_DROP_RATE, WEAPON_GACHA_PACKS
from bot.config.imageMap import WEAPON_IMAGE_MAP  # mapping ảnh vũ khí
from bot.entity.weaponTemplate import WeaponTemplate

class BuyWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="buyweapon", description="Mua gói mở vũ khí và mở hộp ngay lập tức")
    @app_commands.describe(
        pack="Tên gói mở vũ khí (ví dụ: weapon_pack)"
    )
    async def buyWeapon(self, interaction: discord.Interaction, pack: str):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                # Khởi tạo các repository cần thiết
                playerRepo = PlayerRepository(session)
                weaponTemplateRepo = WeaponTemplateRepository(session)
                playerWeaponRepo = PlayerWeaponRepository(session)
                playerService = PlayerService(playerRepo)

                # Kiểm tra tài khoản người chơi
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!")
                    return

                # Kiểm tra gói mở vũ khí hợp lệ
                if pack not in WEAPON_GACHA_PRICES:
                    validPacks = ", ".join(WEAPON_GACHA_PRICES.keys())
                    await interaction.followup.send(f"❌ Gói '{pack}' không hợp lệ. Vui lòng chọn: {validPacks}")
                    return

                # Tính chi phí cho 1 lượt mở gói vũ khí
                cost = WEAPON_GACHA_PRICES[pack]
                if player.coin_balance < cost:
                    await interaction.followup.send(f"❌ Số dư không đủ. Cần {cost:,} Ryo, hiện có {player.coin_balance:,} Ryo.")
                    return

                # Trừ tiền
                playerService.addCoin(playerId, -cost)

                # Roll ngẫu nhiên theo weighted random dựa trên tỉ lệ drop của gói weapon
                rates = WEAPON_GACHA_DROP_RATE[pack]
                tiers = list(rates.keys())
                weights = list(rates.values())
                outcomeTier = random.choices(tiers, weights=weights, k=1)[0]

                # Lấy ngẫu nhiên một weapon template theo grade (outcomeTier)
                weapon = weaponTemplateRepo.getRandomByGrade(outcomeTier)
                if not weapon:
                    await interaction.followup.send("❌ Lỗi khi mở hộp, không tìm thấy vũ khí phù hợp.")
                    return

                # Thêm vũ khí vào kho của người chơi
                playerWeaponRepo.incrementQuantity(playerId, weapon.weapon_key, increment=1)

                # Lấy URL ảnh thực từ WEAPON_IMAGE_MAP (weapon.image_url lưu key)
                imageUrl = WEAPON_IMAGE_MAP.get(weapon.image_url, weapon.image_url)

                # Tạo embed hiển thị thông tin của vũ khí nhận được
                embed = discord.Embed(
                    title=f"🎉 Bạn đã mua gói {pack} và mở được vũ khí: {weapon.name}",
                    description=(
                        f"**Bonus Power:** {weapon.bonus_power}\n"
                        f"**Bậc:** {weapon.grade}\n"
                        f"**Giá bán:** {weapon.sell_price:,} Ryo\n\n"
                        f"Vũ khí đã được thêm vào kho của bạn. Kiểm tra kho bằng lệnh `/inventory`."
                    ),
                    color=discord.Color.green()
                )
                embed.set_image(url=imageUrl)
                await interaction.followup.send(embed=embed)
        except Exception as e:
            print("❌ Lỗi khi xử lý buyweapon:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(BuyWeapon(bot))
