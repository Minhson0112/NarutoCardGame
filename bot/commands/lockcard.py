import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.services.i18n import t


class LockCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="lockcard",
        description="Lock cards"
    )
    @app_commands.describe(
        card_id="card_id"
    )
    async def lockcard(self, interaction: discord.Interaction, card_id: int):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)

                # 1) registered check
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'lockcard.error.not_registered')}",
                        ephemeral=True
                    )
                    return

                # 2) ownership check
                card = cardRepo.getById(card_id)
                if not card or card.player_id != player_id:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'lockcard.error.not_owner', card_id=card_id)}",
                        ephemeral=True
                    )
                    return

                card_name = card.template.name
                card_key = card.card_key

                # 3) get all same cards
                all_same_cards = cardRepo.getByPlayerIdAndCardKey(player_id, card_key)
                if not all_same_cards:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'lockcard.error.not_found_same_type')}",
                        ephemeral=True
                    )
                    return

                # 4) lock all
                for c in all_same_cards:
                    c.locked = True

                session.commit()

                await interaction.followup.send(
                    f"✅ {t(guild_id, 'lockcard.success', card_name=card_name)}"
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý lockcard:", e)
            await interaction.followup.send(
                f"❌ {t(guild_id, 'lockcard.error.generic')}",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(LockCard(bot))
