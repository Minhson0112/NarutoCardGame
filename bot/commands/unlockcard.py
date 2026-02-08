import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.services.i18n import t


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
        guild_id = interaction.guild.id if interaction.guild else None

        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)

                # 1) Kiểm tra người chơi đã đăng ký
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        t(guild_id, "unlockcard.not_registered"),
                        ephemeral=True
                    )
                    return

                # 2) Lấy thẻ theo ID
                card = cardRepo.getById(card_id)
                if not card or card.player_id != player_id:
                    await interaction.followup.send(
                        t(guild_id, "unlockcard.not_owner", card_id=card_id),
                        ephemeral=True
                    )
                    return

                card_name = card.template.name
                card_level = card.level

                # 3) Nếu thẻ đã không bị khoá
                if not getattr(card, "locked", False):
                    await interaction.followup.send(
                        t(
                            guild_id,
                            "unlockcard.already_unlocked",
                            card_name=card_name,
                            card_id=card.id,
                            card_level=card_level
                        ),
                        ephemeral=True
                    )
                    return

                # 4) Mở khoá
                card.locked = False
                session.commit()

                await interaction.followup.send(
                    t(
                        guild_id,
                        "unlockcard.success",
                        card_name=card_name,
                        card_id=card.id,
                        card_level=card_level
                    )
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý unlockcard:", e)
            await interaction.followup.send(
                t(guild_id, "unlockcard.error"),
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(UnlockCard(bot))
