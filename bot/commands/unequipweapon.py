import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository

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
        app_commands.Choice(name="middle",  value="middle"),
        app_commands.Choice(name="back",    value="back"),
    ])
    async def unequipWeapon(
        self,
        interaction: discord.Interaction,
        position: app_commands.Choice[str]
    ):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                setupRepo  = PlayerActiveSetupRepository(session)

                # 1) Kiểm tra người chơi đã đăng ký
                if not playerRepo.getById(player_id):
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Dùng `/register` trước!",
                        ephemeral=True
                    )
                    return

                # 2) Lấy hoặc tạo active setup
                setup = setupRepo.getByPlayerId(player_id)
                if not setup:
                    await interaction.followup.send(
                        "❌ Bạn chưa lắp thẻ nào, không thể tháo vũ khí!",
                        ephemeral=True
                    )
                    return

                slot_map_weapon = {
                    "tanker": "weapon_slot1",
                    "middle": "weapon_slot2",
                    "back":   "weapon_slot3",
                }
                pos = position.value
                weapon_attr = slot_map_weapon[pos]

                # 3) Kiểm xem có vũ khí nào lắp ở slot đó không
                weapon_id = getattr(setup, weapon_attr)
                if weapon_id is None:
                    await interaction.followup.send(
                        f"❌ Hiện không có vũ khí nào ở vị trí **{pos}**.",
                        ephemeral=True
                    )
                    return

                # 4) Gỡ vũ khí: unset equipped và clear slot
                pw = weaponRepo.getById(weapon_id)
                if pw:
                    pw.equipped = False

                # cập nhật slot về None
                if pos == "tanker":
                    setupRepo.updateWeaponSlot1(player_id, None)
                elif pos == "middle":
                    setupRepo.updateWeaponSlot2(player_id, None)
                else:
                    setupRepo.updateWeaponSlot3(player_id, None)

                name = pw.template.name if pw else f"ID {weapon_id}"
                await interaction.followup.send(
                    f"✅ Đã tháo vũ khí **{name}** khỏi **{pos}**.",
                )

        except Exception as e:
            await interaction.followup.send(
                f"❌ Lỗi khi unequipweapon:\n```{e}```",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(UnequipWeapon(bot))
