import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.services.i18n import t


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
        guild_id = interaction.guild.id if interaction.guild else None

        player_id = interaction.user.id
        selected_tier = tier.value

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        t(guild_id, "sellallcard.not_registered")
                    )
                    return

                all_cards = cardRepo.getByPlayerId(player_id)
                matching_cards = [
                    c for c in all_cards
                    if c.template.tier == selected_tier
                ]

                if not matching_cards:
                    await interaction.followup.send(
                        t(guild_id, "sellallcard.no_cards_in_tier", tier=selected_tier)
                    )
                    return

                equipped_cards = [c for c in matching_cards if c.equipped]
                preserve_ids = set()
                for eq in equipped_cards:
                    preserve_ids.add(eq.id)
                    for c in matching_cards:
                        if c.card_key == eq.card_key and c.level < eq.level:
                            preserve_ids.add(c.id)

                sellable_cards = [
                    c for c in matching_cards
                    if c.id not in preserve_ids and not getattr(c, "locked", False)
                ]

                if not sellable_cards:
                    await interaction.followup.send(
                        t(guild_id, "sellallcard.nothing_to_sell")
                    )
                    return

                total_money = 0
                total_quantity = 0
                for card in sellable_cards:
                    card_money = card.template.sell_price * card.level * card.quantity
                    total_money += card_money
                    total_quantity += card.quantity
                    cardRepo.deleteCard(card)

                player.coin_balance += total_money
                dailyTaskRepo.updateShopSell(player_id)
                session.commit()

                await interaction.followup.send(
                    t(
                        guild_id,
                        "sellallcard.success",
                        money=total_money,
                        quantity=total_quantity,
                        tier=selected_tier
                    )
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý sellallcard:", e)
            await interaction.followup.send(
                t(guild_id, "sellallcard.error")
            )


async def setup(bot):
    await bot.add_cog(SellAllCard(bot))
