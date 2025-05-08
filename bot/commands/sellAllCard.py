import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository

class SellAllCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="sellallcard",
        description="Bán toàn bộ các thẻ theo cấp mà bạn chọn để nhận Ryo"
    )
    @app_commands.describe(tier="Loại thẻ bạn muốn bán (Genin, Chunin, Jounin, Kage, Legendary)")
    @app_commands.choices(tier=[
        app_commands.Choice(name="Genin", value="Genin"),
        app_commands.Choice(name="Chunin", value="Chunin"),
        app_commands.Choice(name="Jounin", value="Jounin"),
        app_commands.Choice(name="Kage", value="Kage"),
        app_commands.Choice(name="Legendary", value="Legendary")
    ])
    async def sellallcard(self, interaction: discord.Interaction, tier: app_commands.Choice[str]):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id
        selected_tier = tier.value

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)

                # 1️⃣ Kiểm tra tài khoản
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        "⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!"
                    )
                    return

                # 2️⃣ Lấy tất cả thẻ cùng tier, nhưng chưa loại locked
                all_cards = cardRepo.getByPlayerId(player_id)
                matching_cards = [
                    c for c in all_cards
                    if c.template.tier == selected_tier
                ]

                if not matching_cards:
                    await interaction.followup.send(
                        f"⚠️ Bạn không có thẻ nào thuộc cấp **{selected_tier}**."
                    )
                    return

                # 3️⃣ Xác định thẻ equipped và cấp thấp hơn cần giữ
                equipped_cards = [c for c in matching_cards if c.equipped]
                preserve_ids = set()
                for eq in equipped_cards:
                    preserve_ids.add(eq.id)
                    for c in matching_cards:
                        if c.card_key == eq.card_key and c.level < eq.level:
                            preserve_ids.add(c.id)

                # 4️⃣ Xác định thẻ có thể bán: 
                #    - Không nằm trong preserve_ids
                #    - Và không bị locked
                sellable_cards = [
                    c for c in matching_cards 
                    if c.id not in preserve_ids and not getattr(c, 'locked', False)
                ]
                if not sellable_cards:
                    await interaction.followup.send(
                        "⚠️ Không có thẻ nào để bán — bạn đã giữ lại thẻ đang lắp, cấp thấp hơn hoặc đã khoá."
                    )
                    return

                # 5️⃣ Tính tiền và xóa thẻ
                total_money = 0
                total_quantity = 0
                for card in sellable_cards:
                    card_money = card.template.sell_price * card.level * card.quantity
                    total_money += card_money
                    total_quantity += card.quantity
                    cardRepo.deleteCard(card)

                # 6️⃣ Cộng xu, cập nhật daily task và commit
                player.coin_balance += total_money
                dailyTaskRepo.updateShopSell(player_id)
                session.commit()

                # 7️⃣ Phản hồi kết quả
                await interaction.followup.send(
                    f"✅ Bán thành công! Bạn nhận được **{total_money:,} Ryo** "
                    f"từ việc bán {total_quantity} thẻ cấp **{selected_tier}**."
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý sellallcard:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra. Vui lòng thử lại sau."
            )

async def setup(bot):
    await bot.add_cog(SellAllCard(bot))
