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
        description="Mở khoá một thẻ theo ID"
    )
    @app_commands.describe(
        card_id="ID thẻ bạn muốn mở khoá (xem trong /inventory)"
    )
    async def unlockcard(self, interaction: discord.Interaction, card_id: int):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo   = PlayerCardRepository(session)

                # 1) Kiểm tra người chơi đã đăng ký
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!",
                        ephemeral=True
                    )
                    return

                # 2) Lấy thẻ theo ID
                card = cardRepo.getById(card_id)
                if not card or card.player_id != player_id:
                    await interaction.followup.send(
                        f"⚠️ Bạn không sở hữu thẻ với ID `{card_id}`.",
                        ephemeral=True
                    )
                    return

                # 3) Mở khoá thẻ này
                if not card.locked:
                    await interaction.followup.send(
                        f"ℹ️ Thẻ **{card.template.name}** (ID `{card.id}`, Lv {card.level}) "
                        f"hiện đang không bị khoá.",
                        ephemeral=True
                    )
                    return

                card.locked = False
                session.commit()

                await interaction.followup.send(
                    f"✅ Đã mở khoá thẻ **{card.template.name}** "
                    f"(ID `{card.id}`, Lv {card.level}).\n"
                    f"🔓 Thẻ này giờ có thể bán."
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý unlockcard:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra khi mở khoá thẻ. Vui lòng thử lại sau.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(UnlockCard(bot))
