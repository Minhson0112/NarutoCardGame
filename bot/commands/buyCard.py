import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import checks, CommandOnCooldown
import random

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.gachaPityCounterRepository import GachaPityCounterRepository
from bot.repository.cardTemplateRepository import CardTemplateRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.playerService import PlayerService
from bot.config.gachaConfig import GACHA_PRICES, PITY_LIMIT, PITY_PROTECTION, GACHA_DROP_RATE
from bot.config.imageMap import CARD_IMAGE_MAP
from bot.entity.cardTemplate import CardTemplate
from bot.config.characterSkill import SKILL_MAP

class BuyCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="buycard", description="Mua gói mở thẻ và mở hộp ngay lập tức")
    @app_commands.describe(
        pack="Tên gói mở thẻ (card_basic, card_advanced, card_elite)"
    )
    @app_commands.choices(pack=[
        app_commands.Choice(name="card_basic", value="card_basic"),
        app_commands.Choice(name="card_advanced", value="card_advanced"),
        app_commands.Choice(name="card_elite", value="card_elite")
    ])
    @checks.cooldown(1, 2.0, key=lambda interaction: interaction.user.id)
    async def buyCard(self,interaction: discord.Interaction, pack: str):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                # Khởi tạo các repository cần thiết
                playerRepo = PlayerRepository(session)
                pityRepo = GachaPityCounterRepository(session)
                cardTemplateRepo = CardTemplateRepository(session)
                playerCardRepo = PlayerCardRepository(session)
                playerService = PlayerService(playerRepo)
                dailyTaskRepo = DailyTaskRepository(session)

                # Kiểm tra tài khoản người chơi
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng `/register` trước nhé!")
                    return

                # Kiểm tra gói mở thẻ hợp lệ
                if pack not in GACHA_PRICES:
                    validPacks = ", ".join(GACHA_PRICES.keys())
                    await interaction.followup.send(f"❌ Gói '{pack}' không hợp lệ. Vui lòng chọn: {validPacks}")
                    return

                # Tính chi phí cho 1 lượt mở gói
                cost = GACHA_PRICES[pack]
                if player.coin_balance < cost:
                    await interaction.followup.send(f"❌ Số dư không đủ. Cần {cost:,} Ryo, hiện có {player.coin_balance:,} Ryo.")
                    return

                # Trừ tiền
                playerService.addCoin(playerId, -cost)

                # Hàm mở hộp cho 1 lượt
                def openPack(playerId, pack) -> CardTemplate:
                    counter = pityRepo.getCount(playerId, pack)
                    limit = PITY_LIMIT[pack]
                    protectionTier = PITY_PROTECTION[pack]

                    if counter + 1 >= limit:
                        outcomeTier = protectionTier
                        pityRepo.resetCounter(playerId, pack)
                    else:
                        rates = GACHA_DROP_RATE[pack]
                        tiers = list(rates.keys())
                        weights = list(rates.values())
                        outcomeTier = random.choices(tiers, weights=weights, k=1)[0]
                        pityRepo.incrementCounter(playerId, pack, increment=1)
                    
                    # Lấy ngẫu nhiên card từ bảng card_templates theo tier
                    card = cardTemplateRepo.getRandomByTier(outcomeTier)
                    return card

                card = openPack(playerId, pack)
                if not card:
                    await interaction.followup.send("❌ Lỗi khi mở hộp, không tìm thấy thẻ phù hợp.")
                    return
                
                dailyTaskRepo.updateShopBuy(playerId)
                # Thêm card vào kho của người chơi
                playerCardRepo.incrementQuantity(playerId, card.card_key, increment=1)

                # Lấy URL ảnh thực từ CARD_IMAGE_MAP (card.image_url lưu key)
                imageUrl = CARD_IMAGE_MAP.get(card.image_url, card.image_url)

                skillDescription = SKILL_MAP.get(card.image_url, "Chưa có skill đặc biệt.")

                # Tạo embed hiển thị thông tin của thẻ nhận được
                embed = discord.Embed(
                    title=f"🎉 Bạn đã mua gói {pack} và mở được thẻ: {card.name}",
                    description=(
                        f"**Damage:** {card.base_damage}\n"
                        f"**Hp:** {card.health}\n"
                        f"**Giáp:** {card.armor}\n"
                        f"**Tỉ lệ chí mạng:** {card.crit_rate:.0%}\n"
                        f"**Né:** {card.speed:.0%}\n"
                        f"**chakra gốc:** {card.chakra}\n"
                        f"**Tanker:** {'✅' if card.first_position else '❌'}\n"
                        f"**Bậc:** {card.tier}\n"
                        f"**Hệ chakra:** {card.element}\n"
                        f"**Giá bán:** {card.sell_price:,} Ryo\n\n"
                        f"Thẻ đã được thêm vào kho của bạn. Kiểm tra kho bằng lệnh `/inventory`.\n\n\n\n"
                        f"📜 **Skill đặc biệt:**\n{skillDescription}\n\n"
                    ),
                    color=discord.Color.green()
                )
                embed.set_image(url=imageUrl)
                await interaction.followup.send(embed=embed)
        except Exception as e:
            print("❌ Lỗi khi xử lý buycard:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")
        
    @buyCard.error
    async def buycard_error(self, interaction: discord.Interaction, error):
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                f"⏱️ Bạn phải chờ **{error.retry_after:.1f}** giây nữa mới mở gói tiếp được.",
                ephemeral=True
            )
        else:
            # Với lỗi khác, ta vẫn raise lên để discord.py xử hoặc log
            raise error

async def setup(bot):
    await bot.add_cog(BuyCard(bot))
