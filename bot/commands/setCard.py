import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository

class SetCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setcard", description="Lắp thẻ chiến đấu của bạn")
    @app_commands.describe(card="Tên thẻ bạn sở hữu (ví dụ: Uchiha Madara)")
    async def setCard(self, interaction: discord.Interaction, card: str):
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

                # Lấy repository thẻ và active setup của người chơi
                cardRepo = PlayerCardRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)

                # Tìm tất cả các thẻ của người chơi có tên khớp
                cards = cardRepo.getByCardNameAndPlayerId(playerId, card)
                if not cards:
                    await interaction.followup.send("⚠️ Bạn nhập sai tên thẻ hoặc bạn không sở hữu thẻ đó. Kiểm tra lại trong /inventory.")
                    return

                # Tháo các thẻ đã được cài đặt (unequip tất cả các thẻ của người chơi)
                equippedCards = cardRepo.getEquippedCardsByPlayerId(playerId)
                for equipCard in equippedCards:
                    equipCard.equipped = False

                # Chọn thẻ có cấp độ cao nhất để lắp
                selectedCard = max(cards, key=lambda c: c.level)
                selectedCard.equipped = True

                # Cập nhật active setup của người chơi với thẻ vừa được lắp
                activeSetupRepo.updateActiveCard(playerId, selectedCard.id)

                await interaction.followup.send(
                    f"✅ Đã lắp thẻ **{selectedCard.template.name}** (Cấp Thẻ: {selectedCard.level}). Kiểm tra lại bằng /showprofile"
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý setcard:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(SetCard(bot))
