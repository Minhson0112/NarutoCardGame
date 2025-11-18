import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository

class SellWeapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sellweapon", description="Bán vũ khí của bạn để nhận Ryo")
    @app_commands.describe(
        weaponId="ID của vũ khí muốn bán (xem trong /inventory)",
        quantity="Số lượng vũ khí muốn bán"
    )
    async def sellweapon(self, interaction: discord.Interaction, weaponId: int, quantity: int):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        if quantity <= 0:
            await interaction.followup.send("⚠️ Số lượng vũ khí bán phải lớn hơn 0.")
            return

        try:
            with getDbSession() as session:
                # Lấy thông tin người chơi
                player_repo = PlayerRepository(session)
                weapon_repo = PlayerWeaponRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                # Lấy danh sách các vũ khí của người chơi có tên khớp
                weapon = weapon_repo.getById(weaponId)
                if not weapon or weapon.player_id != player_id:
                    await interaction.followup.send(
                        f"⚠️ Bạn không sở hữu vũ khí với ID `{weaponId}`."
                    )
                    return

                # Kiểm tra nếu có vũ khí đang được cài đặt (equipped)
                if weapon.equipped:
                    await interaction.followup.send(
                        f"⚠️ Vũ khí **{weapon.template.name}** (ID `{weapon.id}`) "
                        f"đang được dùng làm vũ khí chính, hãy tháo vũ khí đó ra "
                        f"bằng lệnh `/unequipweapon` trước khi bán."
                    )
                    return

                weaponName = weapon.template.name
                weaponLevel = weapon.level

                # Tính tổng số lượng vũ khí ở cấp đó
                if weapon.quantity < quantity:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có đủ số lượng vũ khí để bán. "
                        f"Bạn có: {weapon.quantity}, yêu cầu: {quantity}."
                    )
                    return

                # Tính số tiền nhận được: tiền nhận = sell_price * level * quantity
                sell_price  = weapon.template.sell_price
                total_money = sell_price * weapon.level * quantity

                # Tiêu hao các bản ghi vũ khí bán ra:
                weapon.quantity -= quantity
                if weapon.quantity <= 0:
                    weapon_repo.deleteWeapon(weapon)
                # Cộng tiền bán được vào số dư của người chơi
                player.coin_balance += total_money
                dailyTaskRepo.updateShopSell(player_id)
                session.commit()
                await interaction.followup.send(
                    f"✅ Bán thành công! Bạn nhận được **{total_money:,} Ryo** từ việc bán {quantity} vũ khí **{weaponName}** cấp {weaponLevel}."
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý sellweapon:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(SellWeapon(bot))
