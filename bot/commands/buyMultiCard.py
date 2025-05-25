# bot/commands/buy_multicard.py

import random
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from discord.app_commands import checks, CommandOnCooldown

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.gachaPityCounterRepository import GachaPityCounterRepository
from bot.repository.cardTemplateRepository import CardTemplateRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.playerService import PlayerService
from bot.config.gachaConfig import GACHA_PRICES, PITY_LIMIT, PITY_PROTECTION, GACHA_DROP_RATE
from bot.config.config import LEVEL_OPEN_PACK, LEVEL_CONFIG

class BuyMultiCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="buymulticard",
        description="Mua nhiều gói thẻ một lần (chỉ mở từ level 2 trở lên)"
    )
    @app_commands.describe(
        pack="Tên gói mở thẻ (card_basic, card_advanced, card_elite)",
        count="Số pack muốn mua (int)"
    )
    @app_commands.choices(pack=[
        app_commands.Choice(name="card_basic", value="card_basic"),
        app_commands.Choice(name="card_advanced", value="card_advanced"),
        app_commands.Choice(name="card_elite", value="card_elite"),
    ])
    @checks.cooldown(1, 1800.0, key=lambda inter: inter.user.id)
    async def buymulticard(
        self,
        interaction: commands.Context,
        pack: str,
        count: int
    ):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        if count <= 0:
            await interaction.followup.send("⚠️ Số lượng phải lớn hơn 0.")
            return

        try:
            with getDbSession() as session:
                playerRepo    = PlayerRepository(session)
                pityRepo      = GachaPityCounterRepository(session)
                tplRepo       = CardTemplateRepository(session)
                cardRepo      = PlayerCardRepository(session)
                playerService = PlayerService(playerRepo)
                dailyTaskRepo = DailyTaskRepository(session)

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký. Dùng `/register` trước nhé!")
                    return

                # Tính level từ exp
                exp = player.exp or 0
                thresholds = sorted(int(k) for k in LEVEL_CONFIG.keys())
                level = 0
                for t in thresholds:
                    if exp >= t:
                        level = LEVEL_CONFIG[str(t)]
                    else:
                        break

                if level < 2:
                    await interaction.followup.send("⚠️ Chức năng này chỉ dành cho người chơi từ level 2 trở lên.")
                    return

                # Lấy giới hạn mua pack
                max_pack = LEVEL_OPEN_PACK.get(str(level), 0)
                if count > max_pack:
                    await interaction.followup.send(
                        f"⚠️ Bạn ở level {level} chỉ được mua tối đa {max_pack} pack mỗi lần."
                    )
                    return

                # Tính tiền và kiểm tra số dư
                if pack not in GACHA_PRICES:
                    await interaction.followup.send("⚠️ Gói không hợp lệ.")
                    return
                cost_per   = GACHA_PRICES[pack]
                total_cost = cost_per * count
                if player.coin_balance < total_cost:
                    await interaction.followup.send(
                        f"❌ Cần {total_cost:,} Ryo, bạn chỉ có {player.coin_balance:,}."
                    )
                    return

                # Trừ tiền & tăng exp
                playerService.addCoin(player_id, -total_cost)
                playerRepo.incrementExp(player_id, count)

                # Mở pack và cập nhật kho
                results: dict[tuple[str,str], int] = {}
                def open_pack_once():
                    cnt  = pityRepo.getCount(player_id, pack)
                    lim  = PITY_LIMIT[pack]
                    prot = PITY_PROTECTION[pack]
                    if cnt + 1 >= lim:
                        tier = prot
                        pityRepo.resetCounter(player_id, pack)
                    else:
                        rates = GACHA_DROP_RATE[pack]
                        tier  = random.choices(list(rates), weights=list(rates.values()), k=1)[0]
                        pityRepo.incrementCounter(player_id, pack)
                    return tplRepo.getRandomByTier(tier)

                for _ in range(count):
                    card_tpl = open_pack_once()
                    cardRepo.incrementQuantity(player_id, card_tpl.card_key, increment=1)
                    key = (card_tpl.name, card_tpl.tier)
                    results[key] = results.get(key, 0) + 1

                dailyTaskRepo.updateShopBuy(player_id)

                parts = [
                    f"🥷 {name} ({tier}) x {qty}"
                    for (name, tier), qty in results.items()
                ]
                detail = "\n".join(parts)
                await interaction.followup.send(
                    f"✅ Bạn đã mua thành công **{count} {pack}** và nhận được:\n{detail}"
                )
        except Exception as e:
            print("❌ Lỗi buymulticard:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

    @buymulticard.error
    async def buymulticard_error(self, interaction, error):
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                f"⏱️ Chưa hết cooldown, hãy đợi **{error.retry_after:.0f}**s nữa.",
                ephemeral=True
            )
        else:
            raise error

async def setup(bot):
    await bot.add_cog(BuyMultiCard(bot))
