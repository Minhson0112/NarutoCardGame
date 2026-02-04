import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.entity.playerWeapon import PlayerWeapon
from bot.services.i18n import t


class LevelUpWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="levelupweapon",
        description="Upgrade weapon"
    )
    @app_commands.describe(
        weapon_id="weapon_id"
    )
    async def levelUpWeapon(self, interaction: discord.Interaction, weapon_id: int):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                weaponRepo = PlayerWeaponRepository(session)

                # 1) check registered
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send(f"⚠️ {t(guild_id, 'levelupweapon.error.not_registered')}")
                    return

                # 2) get weapon by id & ownership
                mainWeaponCandidate = weaponRepo.getById(weapon_id)
                if not mainWeaponCandidate or mainWeaponCandidate.player_id != playerId:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'levelupweapon.error.not_owner', weapon_id=weapon_id)}"
                    )
                    return

                weapon_name = mainWeaponCandidate.template.name
                current_level = mainWeaponCandidate.level
                desired_level = current_level + 1

                # 3) all same weapon_key for this player
                weapons = weaponRepo.getByPlayerIdAndWeaponKey(playerId, mainWeaponCandidate.weapon_key)
                if not weapons:
                    await interaction.followup.send(f"⚠️ {t(guild_id, 'levelupweapon.error.invalid_data')}")
                    return

                # 4) only upgrade from highest level
                highestLevel = max(w.level for w in weapons)
                if highestLevel != current_level:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'levelupweapon.error.not_highest_level', weapon_id=weapon_id, current_level=current_level, highest_level=highestLevel)}"
                    )
                    return

                # 5) cannot upgrade while equipped
                if mainWeaponCandidate.equipped:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'levelupweapon.error.equipped', weapon_name=weapon_name, weapon_id=mainWeaponCandidate.id)}"
                    )
                    return

                # 6) required materials (level 1) = 3 * current_level
                requiredMaterials = 3 * current_level
                level1Weapons = [w for w in weapons if w.level == 1]
                totalLevel1Quantity = sum(w.quantity for w in level1Weapons)

                if totalLevel1Quantity < requiredMaterials:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'levelupweapon.error.not_enough_materials', weapon_name=weapon_name, required=requiredMaterials, current=totalLevel1Quantity)}"
                    )
                    return

                # 7) consume main weapon (1 copy)
                if mainWeaponCandidate.quantity > 1:
                    mainWeaponCandidate.quantity -= 1
                else:
                    weaponRepo.deleteWeapon(mainWeaponCandidate)

                # 8) create upgraded weapon record
                newWeapon = PlayerWeapon(
                    player_id=playerId,
                    weapon_key=mainWeaponCandidate.weapon_key,
                    level=desired_level,
                    quantity=1,
                    equipped=False
                )
                weaponRepo.create(newWeapon)

                # 9) consume level 1 materials
                remaining = requiredMaterials
                for w in level1Weapons:
                    if remaining <= 0:
                        break
                    if w.quantity <= remaining:
                        remaining -= w.quantity
                        weaponRepo.deleteWeapon(w)
                    else:
                        w.quantity -= remaining
                        if w.quantity == 0:
                            weaponRepo.deleteWeapon(w)
                        remaining = 0

                # 10) exp reward
                playerRepo.incrementExp(playerId, amount=10)

                session.commit()

                await interaction.followup.send(
                    f"✅ {t(guild_id, 'levelupweapon.success', weapon_name=newWeapon.template.name, new_weapon_id=newWeapon.id, from_level=current_level, to_level=desired_level)}"
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý levelupweapon:", e)
            await interaction.followup.send(f"❌ {t(guild_id, 'levelupweapon.error.generic')}")


async def setup(bot):
    await bot.add_cog(LevelUpWeapon(bot))
