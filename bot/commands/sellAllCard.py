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
                # Lấy thông tin người chơi
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                # Lấy tất cả các thẻ của người chơi
                all_cards = cardRepo.getByPlayerId(player_id)
                # Lọc ra các thẻ thuộc cấp được chọn
                matching_cards = [c for c in all_cards if c.template.tier == selected_tier]

                if not matching_cards:
                    await interaction.followup.send(f"⚠️ Bạn không có thẻ nào thuộc cấp **{selected_tier}**.")
                    return

                # Kiểm tra nếu có bất kỳ thẻ nào đang được dùng làm thẻ chính (equipped)
                for c in matching_cards:
                    if c.equipped:
                        await interaction.followup.send(
                            f"⚠️ Thẻ **{c.template.name}** thuộc cấp **{selected_tier}** đang được dùng làm thẻ chính. "
                            f"Vui lòng tháo thẻ đó ra (bằng lệnh /setcard một thẻ khác) trước khi bán toàn bộ thẻ cùng cấp."
                        )
                        return

                total_money = 0
                total_quantity = 0
                # Tính tổng tiền nhận được từ các thẻ và tổng số lượng bán
                for card in matching_cards:
                    # Công thức: sell_price * level * quantity
                    card_money = card.template.sell_price * card.level * card.quantity
                    total_money += card_money
                    total_quantity += card.quantity
                    # Xóa thẻ khỏi kho
                    cardRepo.deleteCard(card)

                # Cộng tiền bán được vào số dư của người chơi
                player.coin_balance += total_money
                
                # Cập nhật nhiệm vụ hằng ngày cho việc bán thẻ
                dailyTaskRepo.updateShopSell(player_id)
                
                session.commit()
                
                await interaction.followup.send(
                    f"✅ Bán thành công! Bạn nhận được **{total_money:,} Ryo** từ việc bán {total_quantity} thẻ cấp **{selected_tier}**."
                )
        except Exception as e:
            print("❌ Lỗi khi xử lý sellallcard:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(SellAllCard(bot))
