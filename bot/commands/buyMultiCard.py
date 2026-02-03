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
from bot.services.i18n import t


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
    async def buymulticard(self, interaction: commands.Context, pack: str, count: int):
        await interaction.response.defer(thinking=True)

        player_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                pityRepo = GachaPityCounterRepository(session)
                tplRepo = CardTemplateRepository(session)
                cardRepo = PlayerCardRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                cooldownRepo = CommandCooldownRepository(session)

                now = datetime.now(timezone.utc)
                last = cooldownRepo.get_last_buy_multicard(player_id)
                if last:
                    if last.tzinfo is None:
                        last = last.replace(tzinfo=timezone.utc)

                    elapsed = now - last
                    if elapsed < timedelta(seconds=1800):
                        remaining = 1800 - int(elapsed.total_seconds())
                        await interaction.followup.send(
                            t(guild_id, "buymulticard.cooldown", remaining=remaining),
                            ephemeral=True
                        )
                        return

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(t(guild_id, "buymulticard.not_registered"))
                    return

                if count <= 0:
                    await interaction.followup.send(t(guild_id, "buymulticard.count_invalid"))
                    return

                exp = player.exp or 0
                thresholds = sorted(int(k) for k in LEVEL_CONFIG.keys())
                level = 0
                for th in thresholds:
                    if exp >= th:
                        level = LEVEL_CONFIG[str(th)]
                    else:
                        break

                if level < 2:
                    await interaction.followup.send(t(guild_id, "buymulticard.level_required"))
                    return

                max_pack = LEVEL_OPEN_PACK.get(str(level), 0)
                if count > max_pack:
                    await interaction.followup.send(
                        t(guild_id, "buymulticard.count_limit", level=level, maxPack=max_pack)
                    )
                    return

                if pack not in GACHA_PRICES:
                    await interaction.followup.send(t(guild_id, "buymulticard.pack_invalid"))
                    return

                cost_per = GACHA_PRICES[pack]
                total_cost = cost_per * count
                if player.coin_balance < total_cost:
                    await interaction.followup.send(
                        t(guild_id, "buymulticard.not_enough_balance", totalCost=total_cost, balance=player.coin_balance)
                    )
                    return

                player.coin_balance -= total_cost
                playerRepo.incrementExp(player_id, count)
                session.commit()

                results: dict[tuple[str, str], int] = {}

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
                    if not card_tpl:
                        continue

                    cardRepo.incrementQuantity(player_id, card_tpl.card_key, increment=1)
                    key = (card_tpl.name, card_tpl.tier)
                    results[key] = results.get(key, 0) + 1

                dailyTaskRepo.updateShopBuy(player_id)
                cooldownRepo.set_last_buy_multicard(player_id, now)

                parts = [
                    t(guild_id, "buymulticard.item_line", name=name, tier=tier, qty=qty)
                    for (name, tier), qty in results.items()
                ]
                detail = "\n".join(parts) if parts else ""

                header = t(guild_id, "buymulticard.success_header", count=count, pack=pack)
                msg = f"{header}\n{detail}" if detail else header

                await interaction.followup.send(msg)

        except Exception as e:
            print("❌ Lỗi buymulticard:", e)
            await interaction.followup.send(t(guild_id, "buymulticard.error"))


async def setup(bot):
    await bot.add_cog(BuyMultiCard(bot))
