import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.services.i18n import t


class SetWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setweapon",
        description="Lắp vũ khí cho vị trí tương ứng với thẻ đã equip"
    )
    @app_commands.describe(
        position="Chọn vị trí lắp: tanker/middle/back (tương ứng với vị trí thẻ)",
        weapon_id="ID vũ khí bạn sở hữu (xem trong /inventory)"
    )
    @app_commands.choices(position=[
        app_commands.Choice(name="tanker", value="tanker"),
        app_commands.Choice(name="middle", value="middle"),
        app_commands.Choice(name="back", value="back"),
    ])
    async def setWeapon(
        self,
        interaction: discord.Interaction,
        position: app_commands.Choice[str],
        weapon_id: int
    ):
        await interaction.response.defer(thinking=True)

        player_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                setupRepo = PlayerActiveSetupRepository(session)

                # 1) Kiểm tra người chơi đã đăng ký
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        t(guild_id, "setweapon.not_registered")
                    )
                    return

                # 2) Lấy vũ khí theo ID
                selected = weaponRepo.getById(weapon_id)
                if not selected or selected.player_id != player_id:
                    await interaction.followup.send(
                        t(guild_id, "setweapon.not_owner", weaponId=weapon_id)
                    )
                    return

                # 3) Lấy hoặc tạo active setup
                setup = setupRepo.getByPlayerId(player_id)
                if not setup:
                    setup = setupRepo.createEmptySetup(player_id)

                # 4) Kiểm vị trí tương ứng có thẻ hay chưa
                slot_map_card = {
                    "tanker": "card_slot1",
                    "middle": "card_slot2",
                    "back": "card_slot3",
                }
                slot_map_weapon = {
                    "tanker": "weapon_slot1",
                    "middle": "weapon_slot2",
                    "back": "weapon_slot3",
                }

                pos = position.value
                card_attr = slot_map_card[pos]
                weapon_attr = slot_map_weapon[pos]

                card_id_in_slot = getattr(setup, card_attr)
                if card_id_in_slot is None:
                    await interaction.followup.send(
                        t(guild_id, "setweapon.no_card_in_slot", position=pos)
                    )
                    return

                # 5) Ngăn lắp trùng vũ khí ở slot khác
                for other_pos, w_attr in slot_map_weapon.items():
                    if other_pos != pos and getattr(setup, w_attr) == selected.id:
                        await interaction.followup.send(
                            t(guild_id, "setweapon.duplicate_weapon"),
                            ephemeral=True
                        )
                        return

                # 6) Unequip vũ khí cũ ở slot hiện tại
                old_weapon_id = getattr(setup, weapon_attr)
                if old_weapon_id is not None:
                    old_weapon = weaponRepo.getById(old_weapon_id)
                    if old_weapon:
                        old_weapon.equipped = False

                # 7) Equip vũ khí mới & cập nhật slot
                selected.equipped = True
                if pos == "tanker":
                    setupRepo.updateWeaponSlot1(player_id, selected.id)
                elif pos == "middle":
                    setupRepo.updateWeaponSlot2(player_id, selected.id)
                else:
                    setupRepo.updateWeaponSlot3(player_id, selected.id)

                await interaction.followup.send(
                    t(
                        guild_id,
                        "setweapon.success",
                        weaponName=selected.template.name,
                        weaponLevel=selected.level,
                        position=pos
                    )
                )

        except Exception as e:
            await interaction.followup.send(
                t(guild_id, "setweapon.error", error=str(e)),
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(SetWeapon(bot))
