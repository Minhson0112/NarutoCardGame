import random
from datetime import datetime, timezone, timedelta
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.gachaPityCounterRepository import GachaPityCounterRepository
from bot.repository.cardTemplateRepository import CardTemplateRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.repository.commandCooldownRepository import CommandCooldownRepository
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
    async def buymulticard(
        self,
        interaction: commands.Context,
        pack: str,
        count: int
    ):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                # repositories
                playerRepo = PlayerRepository(session)
                pityRepo = GachaPityCounterRepository(session)
                tplRepo = CardTemplateRepository(session)
                cardRepo = PlayerCardRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                cooldownRepo = CommandCooldownRepository(session)

                # cooldown logic: 1800s = 30m
                now = datetime.now(timezone.utc)
                last = cooldownRepo.get_last_buy_multicard(player_id)
                if last:
                    # ensure last is timezone-aware
                    if last.tzinfo is None:
                        last = last.replace(tzinfo=timezone.utc)
                    if (now - last) < timedelta(seconds=1800):
                        remaining = 1800 - int((now - last).total_seconds())
                        await interaction.followup.send(
                            f"⏱️ Chưa hết cooldown, hãy đợi **{remaining}**s nữa.",
                            ephemeral=True
                        )
                        return

                # đăng ký
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký. Dùng `/register` trước nhé!")
                    return

                # validate count
                if count <= 0:
                    await interaction.followup.send("⚠️ Số lượng phải lớn hơn 0.")
                    return

                # tính level
                exp = player.exp or 0
                thresholds = sorted(int(k) for k in LEVEL_CONFIG.keys())
                level = 0
                for t in thresholds:
                    if exp >= t:
                        level = LEVEL_CONFIG[str(t)]
                    else:
                        break
                if level < 2:
                    await interaction.followup.send(
                        "⚠️ Chức năng này chỉ dành cho người chơi từ level 2 trở lên."
                    )
                    return

                # giới hạn pack
                max_pack = LEVEL_OPEN_PACK.get(str(level), 0)
                if count > max_pack:
                    await interaction.followup.send(
                        f"⚠️ Bạn ở level {level} chỉ được mua tối đa {max_pack} pack mỗi lần."
                    )
                    return

                # kiểm tra tiền
                if pack not in GACHA_PRICES:
                    await interaction.followup.send("⚠️ Gói không hợp lệ.")
                    return
                cost_per = GACHA_PRICES[pack]
                total_cost = cost_per * count
                if player.coin_balance < total_cost:
                    await interaction.followup.send(
                        f"❌ Cần {total_cost:,} Ryo, bạn chỉ có {player.coin_balance:,}."
                    )
                    return

                # trừ tiền và tăng exp
                player.coin_balance -= total_cost
                playerRepo.incrementExp(player_id, count)
                session.commit()

                # mở pack và cập nhật kho
                results: dict[tuple[str,str], int] = {}
                def open_pack_once():
                    cnt = pityRepo.getCount(player_id, pack)
                    lim = PITY_LIMIT[pack]
                    prot = PITY_PROTECTION[pack]
                    if cnt + 1 >= lim:
                        tier = prot
                        pityRepo.resetCounter(player_id, pack)
                    else:
                        rates = GACHA_DROP_RATE[pack]
                        tier = random.choices(list(rates), weights=list(rates.values()), k=1)[0]
                        pityRepo.incrementCounter(player_id, pack)
                    return tplRepo.getRandomByTier(tier)

                for _ in range(count):
                    card_tpl = open_pack_once()
                    cardRepo.incrementQuantity(player_id, card_tpl.card_key, increment=1)
                    key = (card_tpl.name, card_tpl.tier)
                    results[key] = results.get(key, 0) + 1

                dailyTaskRepo.updateShopBuy(player_id)
                # cập nhật cooldown
                cooldownRepo.set_last_buy_multicard(player_id, now)

                parts = [f"🥷 {name} ({tier}) x {qty}" for (name, tier), qty in results.items()]
                detail = "\n".join(parts)
                await interaction.followup.send(
                    f"✅ Bạn đã mua thành công **{count} {pack}** và nhận được:\n{detail}"
                )
        except Exception as e:
            print("❌ Lỗi buymulticard:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(BuyMultiCard(bot))
