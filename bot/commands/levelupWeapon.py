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

    @app_commands.command(name="levelupweapon", description="Nâng cấp vũ khí của bạn")
    @app_commands.describe(
        weapon="Tên vũ khí bạn sở hữu (ví dụ: Suriken)",
        desired_level="Cấp mong muốn nâng cấp đến (ví dụ: 2, 3, 4, ...)"
    )
    async def levelUpWeapon(self, interaction: discord.Interaction, weapon: str, desired_level: int):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                # Lấy thông tin người chơi
                playerRepo = PlayerRepository(session)
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                # Lấy danh sách các vũ khí của người chơi theo tên
                weaponRepo = PlayerWeaponRepository(session)
                weapons = weaponRepo.getByWeaponNameAndPlayerId(playerId, weapon)
                if not weapons:
                    await interaction.followup.send("⚠️ Bạn không sở hữu vũ khí này hoặc nhập sai tên. Kiểm tra lại trong /inventory.")
                    return

                # Yêu cầu nâng cấp phải từ cấp 2 trở lên
                if desired_level < 2:
                    await interaction.followup.send("⚠️ Cấp nâng phải từ 2 trở lên.")
                    return

                # Kiểm tra: Người chơi chỉ có thể nâng cấp từ vũ khí cao nhất
                highestLevel = max(w.level for w in weapons)
                if highestLevel != desired_level - 1:
                    await interaction.followup.send(
                        f"⚠️ Bạn chỉ có thể nâng cấp từ vũ khí cao nhất. Hiện tại vũ khí cao nhất của bạn là cấp {highestLevel}."
                    )
                    return

                # Xác định yêu cầu:
                # - Vũ khí chính cần có level == desired_level - 1 (và không được đang được dùng làm vũ khí chính).
                # - Nguyên liệu bổ sung: cần số lượng vũ khí cấp 1 bằng 3 * (desired_level - 1)
                requiredMaterials = 3 * (desired_level - 1)
                mainWeaponCandidate = None

                for w in weapons:
                    if w.level == desired_level - 1:
                        if w.equipped:
                            await interaction.followup.send(
                                f"⚠️ Vũ khí **{w.template.name}** đang được dùng làm vũ khí chính, hãy tháo vũ khí đó ra bằng lệnh /setweapon trước khi nâng cấp."
                            )
                            return
                        mainWeaponCandidate = w
                        break

                if mainWeaponCandidate is None:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có vũ khí **{weapon}** ở cấp {desired_level - 1} để nâng cấp lên cấp {desired_level}."
                    )
                    return

                # Đếm số lượng vũ khí cấp 1 làm nguyên liệu
                level1Weapons = [w for w in weapons if w.level == 1]
                totalLevel1Quantity = sum(w.quantity for w in level1Weapons)
                if totalLevel1Quantity < requiredMaterials:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có đủ vũ khí **{weapon}** cấp 1 để nâng cấp. Yêu cầu: {requiredMaterials}, hiện có: {totalLevel1Quantity}."
                    )
                    return

                # Tiêu hao vũ khí chính (một bản sao) để nâng cấp:
                if mainWeaponCandidate.quantity > 1:
                    mainWeaponCandidate.quantity -= 1
                else:
                    weaponRepo.deleteWeapon(mainWeaponCandidate)

                # Tạo bản ghi mới cho vũ khí đã nâng cấp
                # Giả sử các thuộc tính weapon_key, template, ... được sao chép từ mainWeaponCandidate
                newWeapon = PlayerWeapon(
                    player_id=playerId,
                    weapon_key=mainWeaponCandidate.weapon_key,
                    level=desired_level,
                    quantity=1,
                    equipped=False
                )
                weaponRepo.create(newWeapon)

                # Tiêu hao các vũ khí cấp 1 làm nguyên liệu
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
                        
                playerRepo.incrementExp(playerId,amount=10)
                session.commit()
                await interaction.followup.send(
                    f"✅ Nâng cấp thành công! Vũ khí **{newWeapon.template.name}** đã được nâng lên cấp {desired_level}."
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý levelupweapon:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(LevelUpWeapon(bot))
