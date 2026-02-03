import discord
from discord.ext import commands
from discord import app_commands
import random

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.weaponTemplateRepository import WeaponTemplateRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.playerService import PlayerService
from bot.config.weaponGachaConfig import WEAPON_GACHA_PRICES, WEAPON_GACHA_DROP_RATE
from bot.config.imageMap import WEAPON_IMAGE_MAP
from bot.config.weaponSkill import WEAPON_SKILL_MAP
from bot.services.i18n import t


class BuyWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="buyweapon", description="Mua gói mở vũ khí và mở hộp ngay lập tức")
    @app_commands.describe(pack="Tên gói mở vũ khí (ví dụ: weapon_pack)")
    @app_commands.choices(pack=[
        app_commands.Choice(name="weapon_pack", value="weapon_pack")
    ])
    async def buyWeapon(self, interaction: discord.Interaction, pack: str):
        await interaction.response.defer(thinking=True)

        playerId = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                weaponTemplateRepo = WeaponTemplateRepository(session)
                playerWeaponRepo = PlayerWeaponRepository(session)
                playerService = PlayerService(playerRepo)
                dailyTaskRepo = DailyTaskRepository(session)

                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send(t(guild_id, "buyweapon.not_registered"))
                    return

                if pack not in WEAPON_GACHA_PRICES:
                    validPacks = ", ".join(WEAPON_GACHA_PRICES.keys())
                    await interaction.followup.send(
                        t(guild_id, "buyweapon.pack_invalid", pack=pack, validPacks=validPacks)
                    )
                    return

                cost = WEAPON_GACHA_PRICES[pack]
                if player.coin_balance < cost:
                    await interaction.followup.send(
                        t(
                            guild_id,
                            "buyweapon.not_enough_balance",
                            cost=cost,
                            balance=player.coin_balance
                        )
                    )
                    return

                playerService.addCoin(playerId, -cost)
                playerRepo.incrementExp(playerId, amount=20)

                rates = WEAPON_GACHA_DROP_RATE[pack]
                tiers = list(rates.keys())
                weights = list(rates.values())
                outcomeTier = random.choices(tiers, weights=weights, k=1)[0]

                weapon = weaponTemplateRepo.getRandomByGrade(outcomeTier)
                if not weapon:
                    await interaction.followup.send(t(guild_id, "buyweapon.no_weapon_found"))
                    return

                dailyTaskRepo.updateShopBuy(playerId)
                playerWeaponRepo.incrementQuantity(playerId, weapon.weapon_key, increment=1)

                imageUrl = WEAPON_IMAGE_MAP.get(weapon.image_url, weapon.image_url)

                skillDescription = WEAPON_SKILL_MAP.get(weapon.image_url)
                if not skillDescription:
                    skillDescription = t(guild_id, "buyweapon.embed.skill_missing")

                bonus_damage = weapon.bonus_damage or 0
                bonus_health = weapon.bonus_health or 0
                bonus_armor = weapon.bonus_armor or 0
                bonus_crit_rate = weapon.bonus_crit_rate or 0
                bonus_speed = weapon.bonus_speed or 0
                bonus_chakra = weapon.bonus_chakra or 0

                lines = [
                    t(guild_id, "buyweapon.embed.line_bonus_damage", value=bonus_damage),
                    t(guild_id, "buyweapon.embed.line_bonus_health", value=bonus_health),
                    t(guild_id, "buyweapon.embed.line_bonus_armor", value=bonus_armor),
                    t(guild_id, "buyweapon.embed.line_bonus_crit_rate", value=f"{bonus_crit_rate:.0%}"),
                    t(guild_id, "buyweapon.embed.line_bonus_speed", value=f"{bonus_speed:.0%}"),
                    t(guild_id, "buyweapon.embed.line_bonus_chakra", value=bonus_chakra),
                    t(guild_id, "buyweapon.embed.line_grade", grade=weapon.grade),
                    t(guild_id, "buyweapon.embed.line_sell_price", price=weapon.sell_price),
                    "",
                    t(guild_id, "buyweapon.embed.added_to_inventory"),
                    "",
                    "",
                    t(guild_id, "buyweapon.embed.passive_title"),
                    skillDescription,
                    "",
                ]

                embed = discord.Embed(
                    title=t(
                        guild_id,
                        "buyweapon.embed.title",
                        pack=pack,
                        weaponName=weapon.name
                    ),
                    description="\n".join(lines),
                    color=discord.Color.green()
                )
                embed.set_image(url=imageUrl)
                await interaction.followup.send(embed=embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý buyweapon:", e)
            await interaction.followup.send(t(guild_id, "buyweapon.error"))


async def setup(bot):
    await bot.add_cog(BuyWeapon(bot))
