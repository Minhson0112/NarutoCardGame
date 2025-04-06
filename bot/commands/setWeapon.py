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

    @app_commands.command(name="setweapon", description="Lắp vũ khí cho bạn")
    @app_commands.describe(
        weapon="Tên vũ khí bạn sở hữu (ví dụ: Suriken)"
    )
    async def setWeapon(self, interaction: discord.Interaction, weapon: str):
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

                # Lấy repository vũ khí và active setup
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)

                # Tìm tất cả các vũ khí của người chơi có tên khớp
                weapons = weaponRepo.getByWeaponNameAndPlayerId(playerId, weapon)
                if not weapons:
                    await interaction.followup.send("⚠️ Bạn nhập sai tên vũ khí hoặc bạn không sở hữu vũ khí đó.")
                    return

                # Tháo tất cả các vũ khí đang được cài đặt
                equippedWeapons = weaponRepo.getEquippedWeaponsByPlayerId(playerId)
                for equipWeapon in equippedWeapons:
                    equipWeapon.equipped = False

                # Chọn vũ khí có cấp cao nhất để lắp
                selectedWeapon = max(weapons, key=lambda w: w.level)
                selectedWeapon.equipped = True

                # Cập nhật active setup với vũ khí vừa được lắp
                activeSetupRepo.updateActiveWeapon(playerId, selectedWeapon.id)

                await interaction.followup.send(
                    f"✅ Đã lắp vũ khí **{selectedWeapon.template.name}** (Cấp {selectedWeapon.level}). Kiểm tra lại bằng /showprofile"
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý setweapon:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(SetWeapon(bot))
