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
        weapon="Tên vũ khí bạn muốn bán (ví dụ: Suriken)",
        level="Cấp của vũ khí cần bán",
        quantity="Số lượng vũ khí muốn bán"
    )
    async def sellweapon(self, interaction: discord.Interaction, weapon: str, level: int, quantity: int):
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
                weapons = weapon_repo.getByWeaponNameAndPlayerId(player_id, weapon)
                # Lọc các bản ghi có cấp đúng yêu cầu
                matching_weapons = [w for w in weapons if w.level == level]
                if not matching_weapons:
                    await interaction.followup.send(f"⚠️ Bạn không sở hữu vũ khí **{weapon}** ở cấp {level}.")
                    return

                # Kiểm tra nếu có vũ khí đang được cài đặt (equipped)
                for w in matching_weapons:
                    if w.equipped:
                        await interaction.followup.send(
                            f"⚠️ Vũ khí **{w.template.name}** đang được dùng làm vũ khí chính, hãy tháo vũ khí đó ra bằng lệnh /unequipweapon trước khi bán."
                        )
                        return

                # Tính tổng số lượng vũ khí ở cấp đó
                total_quantity = sum(w.quantity for w in matching_weapons)
                if total_quantity < quantity:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có đủ số lượng vũ khí để bán. Bạn có: {total_quantity}, yêu cầu: {quantity}."
                    )
                    return

                # Tính số tiền nhận được: tiền nhận = sell_price * level * quantity
                sell_price = matching_weapons[0].template.sell_price
                total_money = sell_price * level * quantity

                # Tiêu hao các bản ghi vũ khí bán ra:
                remaining = quantity
                for w in matching_weapons:
                    if remaining <= 0:
                        break
                    if w.quantity <= remaining:
                        remaining -= w.quantity
                        weapon_repo.deleteWeapon(w)
                    else:
                        w.quantity -= remaining
                        if w.quantity == 0:
                            weapon_repo.deleteWeapon(w)
                        remaining = 0

                # Cộng tiền bán được vào số dư của người chơi
                player.coin_balance += total_money
                dailyTaskRepo.updateShopSell(player_id)
                session.commit()
                await interaction.followup.send(
                    f"✅ Bán thành công! Bạn nhận được **{total_money:,} Ryo** từ việc bán {quantity} vũ khí **{weapon}** cấp {level}."
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý sellweapon:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(SellWeapon(bot))
