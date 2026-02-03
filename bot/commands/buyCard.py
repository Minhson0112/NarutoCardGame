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
from bot.services.i18n import t


class BuyCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="buycard", description="Mua gói mở thẻ và mở hộp ngay lập tức")
    @app_commands.describe(pack="Tên gói mở thẻ (card_basic, card_advanced, card_elite)")
    @app_commands.choices(pack=[
        app_commands.Choice(name="card_basic", value="card_basic"),
        app_commands.Choice(name="card_advanced", value="card_advanced"),
        app_commands.Choice(name="card_elite", value="card_elite")
    ])
    @checks.cooldown(1, 2.0, key=lambda interaction: interaction.user.id)
    async def buyCard(self, interaction: discord.Interaction, pack: str):
        await interaction.response.defer(thinking=True)

        playerId = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                pityRepo = GachaPityCounterRepository(session)
                cardTemplateRepo = CardTemplateRepository(session)
                playerCardRepo = PlayerCardRepository(session)
                playerService = PlayerService(playerRepo)
                dailyTaskRepo = DailyTaskRepository(session)

                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send(t(guild_id, "buycard.not_registered"))
                    return

                if pack not in GACHA_PRICES:
                    validPacks = ", ".join(GACHA_PRICES.keys())
                    await interaction.followup.send(
                        t(guild_id, "buycard.invalid_pack", pack=pack, validPacks=validPacks)
                    )
                    return

                cost = GACHA_PRICES[pack]
                if player.coin_balance < cost:
                    await interaction.followup.send(
                        t(guild_id, "buycard.not_enough_balance", cost=cost, balance=player.coin_balance)
                    )
                    return

                playerService.addCoin(playerId, -cost)
                playerRepo.incrementExp(playerId)

                def openPack(pid, pack_name) -> CardTemplate:
                    counter = pityRepo.getCount(pid, pack_name)
                    limit = PITY_LIMIT[pack_name]
                    protectionTier = PITY_PROTECTION[pack_name]

                    if counter + 1 >= limit:
                        outcomeTier = protectionTier
                        pityRepo.resetCounter(pid, pack_name)
                    else:
                        rates = GACHA_DROP_RATE[pack_name]
                        tiers = list(rates.keys())
                        weights = list(rates.values())
                        outcomeTier = random.choices(tiers, weights=weights, k=1)[0]
                        pityRepo.incrementCounter(pid, pack_name, increment=1)

                    return cardTemplateRepo.getRandomByTier(outcomeTier)

                card = openPack(playerId, pack)
                if not card:
                    await interaction.followup.send(t(guild_id, "buycard.open_pack_not_found"))
                    return

                dailyTaskRepo.updateShopBuy(playerId)
                playerCardRepo.incrementQuantity(playerId, card.card_key, increment=1)

                imageUrl = CARD_IMAGE_MAP.get(card.image_url, card.image_url)
                skillDescription = SKILL_MAP.get(card.image_url, t(guild_id, "buycard.skill_missing"))

                yes = t(guild_id, "buycard.common.yes")
                no = t(guild_id, "buycard.common.no")
                tanker_value = yes if card.first_position else no

                crit_rate_text = f"{card.crit_rate:.0%}"
                dodge_text = f"{card.speed:.0%}"

                desc_lines = [
                    t(guild_id, "buycard.result.stats.damage", value=card.base_damage),
                    t(guild_id, "buycard.result.stats.hp", value=card.health),
                    t(guild_id, "buycard.result.stats.armor", value=card.armor),
                    t(guild_id, "buycard.result.stats.crit_rate", value=crit_rate_text),
                    t(guild_id, "buycard.result.stats.dodge", value=dodge_text),
                    t(guild_id, "buycard.result.stats.base_chakra", value=card.chakra),
                    t(guild_id, "buycard.result.stats.tanker", value=tanker_value),
                    t(guild_id, "buycard.result.stats.tier", value=card.tier),
                    t(guild_id, "buycard.result.stats.element", value=card.element),
                    t(guild_id, "buycard.result.stats.sell_price", value=card.sell_price),
                    "",
                    t(guild_id, "buycard.result.added_to_inventory"),
                    "",
                    t(guild_id, "buycard.result.skill_title"),
                    f"{skillDescription}",
                ]

                embed = discord.Embed(
                    title=t(guild_id, "buycard.result.title", pack=pack, cardName=card.name),
                    description="\n".join(desc_lines),
                    color=discord.Color.green()
                )
                embed.set_image(url=imageUrl)

                await interaction.followup.send(embed=embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý buycard:", e)
            await interaction.followup.send(t(guild_id, "buycard.error"))

    @buyCard.error
    async def buycard_error(self, interaction: discord.Interaction, error):
        guild_id = interaction.guild.id if interaction.guild else None

        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                t(guild_id, "buycard.cooldown", seconds=error.retry_after),
                ephemeral=True
            )
            return

        raise error


async def setup(bot):
    await bot.add_cog(BuyCard(bot))
