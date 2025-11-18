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
        description="Khoá toàn bộ thẻ cùng loại, thẻ bị khoá sẽ không thể bán"
    )
    @app_commands.describe(
        card_id="ID thẻ bạn muốn khoá (xem trong /inventory)"
    )
    async def lockcard(self, interaction: discord.Interaction, card_id: int):
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

                card_name = card.template.name
                card_key  = card.card_key

                # 3) Lấy toàn bộ thẻ cùng card_key của player
                all_same_cards = cardRepo.getByPlayerIdAndCardKey(player_id, card_key)
                if not all_same_cards:
                    # Về lý thuyết không xảy ra, nhưng cứ phòng lỗi
                    await interaction.followup.send(
                        "⚠️ Không tìm thấy các bản thẻ cùng loại để khoá.",
                        ephemeral=True
                    )
                    return

                # 4) Khoá toàn bộ
                for c in all_same_cards:
                    c.locked = True

                session.commit()

                await interaction.followup.send(
                    f"✅ Đã khoá **toàn bộ thẻ `{card_name}`** của bạn "
                    f"(bao gồm mọi cấp độ & phôi)."
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý lockcard:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra khi khoá thẻ. Vui lòng thử lại sau.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(LockCard(bot))
