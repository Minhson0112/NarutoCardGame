import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.i18n import t


class SellWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sellweapon", description="Bán vũ khí của bạn để nhận Ryo")
    @app_commands.describe(
        weapon_id="ID của vũ khí muốn bán (xem trong /inventory)",
        quantity="Số lượng vũ khí muốn bán"
    )
    async def sellweapon(self, interaction: discord.Interaction, weapon_id: int, quantity: int):
        await interaction.response.defer(thinking=True)

        guild_id = interaction.guild.id if interaction.guild else None
        player_id = interaction.user.id

        if quantity <= 0:
            await interaction.followup.send(
                t(guild_id, "sellweapon.quantity_must_be_positive")
            )
            return

        try:
            with getDbSession() as session:
                player_repo = PlayerRepository(session)
                weapon_repo = PlayerWeaponRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)

                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        t(guild_id, "sellweapon.not_registered")
                    )
                    return

                weapon = weapon_repo.getById(weapon_id)
                if not weapon or weapon.player_id != player_id:
                    await interaction.followup.send(
                        t(guild_id, "sellweapon.not_owner", weaponId=weapon_id)
                    )
                    return

                weaponName = weapon.template.name
                weaponLevel = weapon.level

                if weapon.equipped:
                    await interaction.followup.send(
                        t(
                            guild_id,
                            "sellweapon.equipped",
                            weaponName=weaponName,
                            weaponId=weapon.id
                        )
                    )
                    return

                if weapon.quantity < quantity:
                    await interaction.followup.send(
                        t(
                            guild_id,
                            "sellweapon.not_enough_quantity",
                            current=weapon.quantity,
                            requested=quantity
                        )
                    )
                    return

                sell_price = weapon.template.sell_price
                total_money = sell_price * weapon.level * quantity

                weapon.quantity -= quantity
                if weapon.quantity <= 0:
                    weapon_repo.deleteWeapon(weapon)

                player.coin_balance += total_money
                dailyTaskRepo.updateShopSell(player_id)
                session.commit()

                await interaction.followup.send(
                    t(
                        guild_id,
                        "sellweapon.success",
                        money=total_money,
                        quantity=quantity,
                        weaponName=weaponName,
                        weaponLevel=weaponLevel
                    )
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý sellweapon:", e)
            await interaction.followup.send(
                t(guild_id, "sellweapon.error")
            )


async def setup(bot):
    await bot.add_cog(SellWeapon(bot))
