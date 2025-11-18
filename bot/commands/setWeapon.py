import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository

class SetWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setweapon",
        description="Lắp vũ khí cho vị trí tương ứng với thẻ đã equip"
    )
    @app_commands.describe(
        position="Chọn vị trí lắp: tanker/middle/back (tương ứng với vị trí thẻ)",
        weaponId="ID vũ khí bạn sở hữu (xem trong /inventory)"
    )
    @app_commands.choices(position=[
        app_commands.Choice(name="tanker", value="tanker"),
        app_commands.Choice(name="middle",  value="middle"),
        app_commands.Choice(name="back",    value="back"),
    ])
    async def setWeapon(
        self,
        interaction: discord.Interaction,
        position: app_commands.Choice[str],
        weaponId: int
    ):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                setupRepo  = PlayerActiveSetupRepository(session)

                # 1) Kiểm tra người chơi đã đăng ký
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Dùng `/register` trước!"
                    )
                    return

                # 2) Lấy tất cả vũ khí matching tên
                selected = weaponRepo.getById(weaponId)
                if not selected or selected.player_id != player_id:
                    await interaction.followup.send(
                        f"⚠️ Bạn không sở hữu vũ khí với ID `{weaponId}`."
                    )
                    return

                # 4) Lấy hoặc tạo active setup
                setup = setupRepo.getByPlayerId(player_id)
                if not setup:
                    setup = setupRepo.createEmptySetup(player_id)

                # 5) Kiểm vị trí tương ứng có thẻ hay chưa
                slot_map_card = {
                    "tanker": "card_slot1",
                    "middle": "card_slot2",
                    "back":   "card_slot3",
                }
                slot_map_weapon = {
                    "tanker": "weapon_slot1",
                    "middle": "weapon_slot2",
                    "back":   "weapon_slot3",
                }
                pos = position.value
                card_attr   = slot_map_card[pos]
                weapon_attr = slot_map_weapon[pos]

                card_id_in_slot = getattr(setup, card_attr)
                if card_id_in_slot is None:
                    await interaction.followup.send(
                        f"❌ Không thể lắp vũ khí vào vị trí **{pos}** khi chưa có thẻ tương ứng."
                    )
                    return

                # 6) Ngăn lắp trùng vũ khí ở slot khác
                for other_pos, w_attr in slot_map_weapon.items():
                    if other_pos != pos and getattr(setup, w_attr) == selected.id:
                        await interaction.followup.send(
                            "❌ Vũ khí này đã được lắp ở vị trí khác, không thể lắp trùng!",
                            ephemeral=True
                        )
                        return

                # 7) Unequip vũ khí cũ ở slot hiện tại
                old_weapon_id = getattr(setup, weapon_attr)
                if old_weapon_id is not None:
                    old_weapon = weaponRepo.getById(old_weapon_id)
                    if old_weapon:
                        old_weapon.equipped = False

                # 8) Equip vũ khí mới & cập nhật slot
                selected.equipped = True
                if pos == "tanker":
                    setupRepo.updateWeaponSlot1(player_id, selected.id)
                elif pos == "middle":
                    setupRepo.updateWeaponSlot2(player_id, selected.id)
                else:  # back
                    setupRepo.updateWeaponSlot3(player_id, selected.id)

                await interaction.followup.send(
                    f"✅ Đã lắp vũ khí **{selected.template.name}** (Lv {selected.level}) vào **{pos}**."
                )

        except Exception as e:
            # Debug lỗi nếu cần
            await interaction.followup.send(
                f"❌ Lỗi khi setweapon:\n```{e}```",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(SetWeapon(bot))
