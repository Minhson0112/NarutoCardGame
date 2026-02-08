import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.services.i18n import t


class UnequipWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="unequipweapon",
        description="Tháo vũ khí khỏi vị trí đã lắp"
    )
    @app_commands.describe(
        position="Chọn vị trí tháo: tanker/middle/back"
    )
    @app_commands.choices(position=[
        app_commands.Choice(name="tanker", value="tanker"),
        app_commands.Choice(name="middle", value="middle"),
        app_commands.Choice(name="back", value="back"),
    ])
    async def unequipWeapon(
        self,
        interaction: discord.Interaction,
        position: app_commands.Choice[str]
    ):
        guild_id = interaction.guild.id if interaction.guild else None
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                setupRepo = PlayerActiveSetupRepository(session)

                # 1) Kiểm tra người chơi đã đăng ký
                if not playerRepo.getById(player_id):
                    await interaction.followup.send(
                        t(guild_id, "unequipweapon.not_registered"),
                        ephemeral=True
                    )
                    return

                # 2) Lấy active setup
                setup = setupRepo.getByPlayerId(player_id)
                if not setup:
                    await interaction.followup.send(
                        t(guild_id, "unequipweapon.no_setup"),
                        ephemeral=True
                    )
                    return

                slot_map_weapon = {
                    "tanker": "weapon_slot1",
                    "middle": "weapon_slot2",
                    "back": "weapon_slot3",
                }
                pos = position.value
                weapon_attr = slot_map_weapon[pos]

                # 3) Kiểm slot có vũ khí không
                weapon_id = getattr(setup, weapon_attr)
                if weapon_id is None:
                    await interaction.followup.send(
                        t(guild_id, "unequipweapon.empty_slot", pos=pos),
                        ephemeral=True
                    )
                    return

                # 4) Gỡ vũ khí
                pw = weaponRepo.getById(weapon_id)
                if pw:
                    pw.equipped = False

                if pos == "tanker":
                    setupRepo.updateWeaponSlot1(player_id, None)
                elif pos == "middle":
                    setupRepo.updateWeaponSlot2(player_id, None)
                else:
                    setupRepo.updateWeaponSlot3(player_id, None)

                name = pw.template.name if pw else f"ID {weapon_id}"
                await interaction.followup.send(
                    t(guild_id, "unequipweapon.success", name=name, pos=pos)
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý /unequipweapon:", e)
            await interaction.followup.send(
                t(guild_id, "unequipweapon.error"),
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(UnequipWeapon(bot))
