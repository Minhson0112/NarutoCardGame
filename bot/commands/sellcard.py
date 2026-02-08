import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.i18n import t


class SellCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sellcard", description="Bán thẻ của bạn để nhận Ryo")
    @app_commands.describe(
        card_id="ID của thẻ muốn bán (xem bằng /inventory)",
        quantity="Số lượng thẻ muốn bán"
    )
    async def sellcard(self, interaction: discord.Interaction, card_id: int, quantity: int):
        await interaction.response.defer(thinking=True)

        guild_id = interaction.guild.id if interaction.guild else None
        player_id = interaction.user.id

        if quantity <= 0:
            await interaction.followup.send(
                t(guild_id, "sellcard.quantity_must_be_positive")
            )
            return

        try:
            with getDbSession() as session:
                player_repo = PlayerRepository(session)
                card_repo = PlayerCardRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)

                player = player_repo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        t(guild_id, "sellcard.not_registered")
                    )
                    return

                card = card_repo.getById(card_id)
                if not card or card.player_id != player_id:
                    await interaction.followup.send(
                        t(guild_id, "sellcard.not_owner", cardId=card_id)
                    )
                    return

                cardName = card.template.name
                cardLevel = card.level

                if getattr(card, "locked", False):
                    await interaction.followup.send(
                        t(
                            guild_id,
                            "sellcard.locked",
                            cardName=cardName,
                            cardId=card.id
                        )
                    )
                    return

                if card.equipped:
                    await interaction.followup.send(
                        t(
                            guild_id,
                            "sellcard.equipped",
                            cardName=cardName,
                            cardId=card.id
                        )
                    )
                    return

                if card.quantity < quantity:
                    await interaction.followup.send(
                        t(
                            guild_id,
                            "sellcard.not_enough_quantity",
                            current=card.quantity,
                            requested=quantity
                        )
                    )
                    return

                sell_price = card.template.sell_price
                total_money = sell_price * card.level * quantity

                card.quantity -= quantity
                if card.quantity <= 0:
                    card_repo.deleteCard(card)

                player.coin_balance += total_money
                dailyTaskRepo.updateShopSell(player_id)
                session.commit()

                await interaction.followup.send(
                    t(
                        guild_id,
                        "sellcard.success",
                        money=total_money,
                        quantity=quantity,
                        cardName=cardName,
                        cardLevel=cardLevel
                    )
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý sellcard:", e)
            await interaction.followup.send(
                t(guild_id, "sellcard.error")
            )


async def setup(bot):
    await bot.add_cog(SellCard(bot))
