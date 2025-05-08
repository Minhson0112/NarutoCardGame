import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository

class UnlockCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="unlockcard",
        description="Mở khoá theo tên thẻ"
    )
    @app_commands.describe(
        card_name="Tên thẻ bạn muốn mở khoá (ví dụ: Naruto)"
    )
    async def unlockcard(self, interaction: discord.Interaction, card_name: str):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)

                # Kiểm tra người chơi đã đăng ký
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
                        ephemeral=True
                    )
                    return

                # Lấy các bản ghi thẻ theo tên
                cards = cardRepo.getByCardNameAndPlayerId(player_id, card_name)
                if not cards:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có thẻ nào tên **{card_name}**.",
                        ephemeral=True
                    )
                    return

                # Mở khoá tất cả bản ghi có cùng card_key
                for card in cards:
                    card.locked = False

                session.commit()

                await interaction.followup.send(
                    f"✅ Đã mở khoá thành công {len(cards)} thẻ có tên **{card_name}**."
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý unlockcard:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra khi mở khoá thẻ. Vui lòng thử lại sau.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(UnlockCard(bot))