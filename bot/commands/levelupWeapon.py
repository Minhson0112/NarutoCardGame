import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.entity.playerWeapon import PlayerWeapon

class LevelUpWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="levelupweapon",
        description="Nâng cấp vũ khí của bạn (tăng 1 cấp)"
    )
    @app_commands.describe(
        weapon_id="ID vũ khí bạn muốn nâng cấp (xem trong /inventory)"
    )
    async def levelUpWeapon(self, interaction: discord.Interaction, weapon_id: int):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo  = PlayerRepository(session)
                weaponRepo  = PlayerWeaponRepository(session)

                # 1) Kiểm tra người chơi đã đăng ký
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!"
                    )
                    return

                # 2) Lấy vũ khí theo ID
                mainWeaponCandidate = weaponRepo.getById(weapon_id)
                if not mainWeaponCandidate or mainWeaponCandidate.player_id != playerId:
                    await interaction.followup.send(
                        f"⚠️ Bạn không sở hữu vũ khí với ID `{weapon_id}`. Kiểm tra lại trong /inventory."
                    )
                    return

                weapon_name   = mainWeaponCandidate.template.name
                current_level = mainWeaponCandidate.level
                desired_level = current_level + 1

                # Nếu muốn giới hạn max level thì thêm check ở đây (vd: >50)

                # 3) Lấy tất cả các bản ghi cùng weapon_key của player
                weapons = weaponRepo.getByPlayerIdAndWeaponKey(
                    playerId,
                    mainWeaponCandidate.weapon_key
                )
                if not weapons:
                    await interaction.followup.send(
                        "⚠️ Dữ liệu vũ khí không hợp lệ. Vui lòng thử lại sau."
                    )
                    return

                # 4) Chỉ cho nâng từ vũ khí cấp cao nhất
                highestLevel = max(w.level for w in weapons)
                if highestLevel != current_level:
                    await interaction.followup.send(
                        f"⚠️ Bạn chỉ có thể nâng cấp từ vũ khí cấp cao nhất.\n"
                        f"Vũ khí với ID `{weapon_id}` đang ở cấp {current_level}, "
                        f"nhưng vũ khí cao nhất của bạn là cấp {highestLevel}."
                    )
                    return

                # 5) Vũ khí chính không được đang equipped
                if mainWeaponCandidate.equipped:
                    await interaction.followup.send(
                        f"⚠️ Vũ khí **{weapon_name}** (ID `{mainWeaponCandidate.id}`) "
                        f"đang được trang bị, hãy tháo nó ra bằng lệnh /unequipweapon trước khi nâng cấp."
                    )
                    return

                # 6) Tính nguyên liệu phôi (vũ khí cấp 1)
                # Giữ logic như thẻ: requiredMaterials = 3 * (desired_level - 1)
                # => requiredMaterials = 3 * current_level
                requiredMaterials = 3 * current_level

                level1Weapons = [w for w in weapons if w.level == 1]
                totalLevel1Quantity = sum(w.quantity for w in level1Weapons)

                if totalLevel1Quantity < requiredMaterials:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có đủ vũ khí **{weapon_name}** cấp 1 để nâng cấp.\n"
                        f"Yêu cầu: {requiredMaterials}, hiện có: {totalLevel1Quantity}."
                    )
                    return

                # 7) Tiêu hao vũ khí chính (1 bản)
                if mainWeaponCandidate.quantity > 1:
                    mainWeaponCandidate.quantity -= 1
                else:
                    weaponRepo.deleteWeapon(mainWeaponCandidate)

                # 8) Tạo bản ghi mới cho vũ khí đã nâng cấp
                newWeapon = PlayerWeapon(
                    player_id=playerId,
                    weapon_key=mainWeaponCandidate.weapon_key,
                    level=desired_level,
                    quantity=1,
                    equipped=False
                )
                weaponRepo.create(newWeapon)

                # 9) Tiêu hao vũ khí cấp 1 làm phôi
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

                # 10) Thưởng exp
                playerRepo.incrementExp(playerId, amount=10)

                session.commit()
                await interaction.followup.send(
                    f"✅ Nâng cấp thành công! Vũ khí **{newWeapon.template.name}** "
                    f"(ID `{newWeapon.id}`) đã được nâng từ cấp {current_level} lên cấp {desired_level}."
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý levelupweapon:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra. Vui lòng thử lại sau."
            )

async def setup(bot):
    await bot.add_cog(LevelUpWeapon(bot))
