import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository

class SellCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sellcard", description="Bán thẻ của bạn để nhận Ryo")
    @app_commands.describe(
        cardId="ID của thẻ muốn bán (xem bằng /inventory)",
        quantity="Số lượng thẻ muốn bán"
    )
    async def sellcard(self, interaction: discord.Interaction, cardId: int, quantity: int):
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
                dailyTaskRepo = DailyTaskRepository(session)
                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                # Lấy danh sách các thẻ của người chơi có tên khớp
                card = card_repo.getById(cardId)
                # Lọc các bản ghi có cấp đúng yêu cầu
                if not card or card.player_id != player_id:
                    await interaction.followup.send(f"⚠️ Bạn không sở hữu thẻ với ID `{cardId}`.")
                    return

                cardName = card.template.name
                cardLevel = card.level

                # MỚI: kiểm tra xem có thẻ nào đang bị khoá không
                if getattr(card, "locked", False):
                    await interaction.followup.send(
                        f"🔒 Thẻ **{card.template.name}** (ID `{card.id}`) đang bị khoá.\n"
                        f"Hãy mở khoá bằng lệnh `/unlockcard` trước khi bán."
                    )
                    return

                if card.equipped:
                    await interaction.followup.send(
                        f"⚠️ Thẻ **{card.template.name}** (ID `{card.id}`) đang được dùng trong đội hình.\n"
                        f"Hãy tháo thẻ đó ra bằng lệnh `/setcard` một thẻ khác trước khi bán."
                    )
                    return

                if card.quantity < quantity:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có đủ số lượng để bán. "
                        f"Hiện có: {card.quantity}, yêu cầu: {quantity}."
                    )
                    return

                # Tính số tiền nhận được
                sell_price = card.template.sell_price
                total_money = sell_price * card.level * quantity

                card.quantity -= quantity
                if card.quantity <= 0:
                    card_repo.deleteCard(card)
                # Cộng tiền
                player.coin_balance += total_money

                dailyTaskRepo.updateShopSell(player_id)
                session.commit()

                await interaction.followup.send(
                    f"✅ Bán thành công! Bạn nhận được **{total_money:,} Ryo** "
                    f"từ việc bán {quantity} thẻ **{cardName}** cấp {cardLevel}."
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý sellcard:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(SellCard(bot))
