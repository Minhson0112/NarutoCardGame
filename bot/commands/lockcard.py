import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository

class LockCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="lockcard",
        description="Khoá tất cả thẻ của bạn, thẻ bị khoá sẽ không thể bán"
    )
    @app_commands.describe(
        card_name="Tên thẻ bạn muốn khoá (ví dụ: Naruto)"
    )
    async def lockcard(self, interaction: discord.Interaction, card_name: str):
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

                # Khoá tất cả bản ghi có cùng card_key
                for card in cards:
                    card.locked = True

                session.commit()

                await interaction.followup.send(
                    f"✅ Đã khoá thành công thẻ có tên **{card_name}**."
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý lockcard:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra khi khoá thẻ. Vui lòng thử lại sau.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(LockCard(bot))