import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository

class SellCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sellcard", description="Bán thẻ của bạn để nhận Ryo")
    @app_commands.describe(
        card="Tên thẻ bạn muốn bán (ví dụ: Uchiha Madara)",
        level="Cấp của thẻ cần bán",
        quantity="Số lượng thẻ muốn bán"
    )
    async def sellcard(self, interaction: discord.Interaction, card: str, level: int, quantity: int):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        if quantity <= 0:
            await interaction.followup.send("⚠️ Số lượng thẻ bán phải lớn hơn 0.")
            return

        try:
            with getDbSession() as session:
                # Lấy thông tin người chơi
                player_repo = PlayerRepository(session)
                card_repo = PlayerCardRepository(session)
                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                # Lấy danh sách các thẻ của người chơi có tên khớp
                cards = card_repo.getByCardNameAndPlayerId(player_id, card)
                # Lọc các bản ghi có cấp đúng yêu cầu
                matching_cards = [c for c in cards if c.level == level]
                if not matching_cards:
                    await interaction.followup.send(f"⚠️ Bạn không sở hữu thẻ **{card}** ở cấp {level}.")
                    return

                # Kiểm tra nếu có thẻ nào đang được dùng làm thẻ chính (equipped)
                for c in matching_cards:
                    if c.equipped:
                        await interaction.followup.send(
                            f"⚠️ Thẻ **{c.template.name}** đang được dùng làm thẻ chính, hãy tháo thẻ đó ra bằng lệnh /setcard một thẻ khác trước khi bán."
                        )
                        return

                # Tính tổng số lượng thẻ ở cấp đó
                total_quantity = sum(c.quantity for c in matching_cards)
                if total_quantity < quantity:
                    await interaction.followup.send(f"⚠️ Bạn không có đủ số lượng thẻ để bán. Bạn có: {total_quantity}, yêu cầu: {quantity}.")
                    return

                # Tính số tiền nhận được: tiền nhận = sell_price * cấp thẻ * số lượng bán
                # Giả sử sell_price được lấy từ template của bản ghi đầu tiên
                sell_price = matching_cards[0].template.sell_price
                total_money = sell_price * level * quantity

                # Tiêu hao các bản ghi thẻ bán ra:
                remaining = quantity
                for c in matching_cards:
                    if remaining <= 0:
                        break
                    if c.quantity <= remaining:
                        remaining -= c.quantity
                        card_repo.deleteCard(c)
                    else:
                        c.quantity -= remaining
                        if c.quantity == 0:
                            card_repo.deleteCard(c)
                        remaining = 0

                # Cộng tiền bán được vào số dư của người chơi
                player.coin_balance += total_money

                session.commit()
                await interaction.followup.send(
                    f"✅ Bán thành công! Bạn nhận được **{total_money:,} Ryo** từ việc bán {quantity} thẻ **{card}** cấp {level}."
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý sellcard:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(SellCard(bot))
