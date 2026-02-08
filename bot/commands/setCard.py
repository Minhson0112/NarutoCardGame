import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.services.i18n import t


class SetCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setcard",
        description="Lắp thẻ chiến đấu của bạn vào một vị trí cụ thể"
    )
    @app_commands.describe(
        position="Chọn vị trí lắp: tanker/middle/back",
        card_id="ID thẻ bạn sở hữu (xem trong /inventory)"
    )
    @app_commands.choices(position=[
        app_commands.Choice(name="tanker", value="tanker"),
        app_commands.Choice(name="middle", value="middle"),
        app_commands.Choice(name="back", value="back"),
    ])
    async def setCard(
        self,
        interaction: discord.Interaction,
        position: app_commands.Choice[str],
        card_id: int
    ):
        await interaction.response.defer(thinking=True)

        guild_id = interaction.guild.id if interaction.guild else None
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                setupRepo = PlayerActiveSetupRepository(session)

                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send(
                        t(guild_id, "setcard.not_registered")
                    )
                    return

                selected = cardRepo.getById(card_id)
                if not selected or selected.player_id != player_id:
                    await interaction.followup.send(
                        t(guild_id, "setcard.not_owner", cardId=card_id)
                    )
                    return

                pos = position.value
                is_first = selected.template.first_position

                if pos == "tanker" and not is_first:
                    await interaction.followup.send(
                        t(guild_id, "setcard.invalid_tanker")
                    )
                    return

                if pos in ("middle", "back") and is_first:
                    await interaction.followup.send(
                        t(guild_id, "setcard.must_be_tanker")
                    )
                    return

                setup = setupRepo.getByPlayerId(player_id)
                if not setup:
                    setup = setupRepo.createEmptySetup(player_id)

                slot_map = {
                    "tanker": "card_slot1",
                    "middle": "card_slot2",
                    "back": "card_slot3"
                }
                cur_attr = slot_map[pos]

                for other_pos, attr in slot_map.items():
                    if other_pos != pos and getattr(setup, attr) == selected.id:
                        await interaction.followup.send(
                            t(guild_id, "setcard.duplicate_slot"),
                            ephemeral=True
                        )
                        return

                old_id = getattr(setup, cur_attr)
                if old_id is not None:
                    old_card = cardRepo.getById(old_id)
                    if old_card:
                        old_card.equipped = False

                selected.equipped = True
                if pos == "tanker":
                    setupRepo.updateCardSlot1(player_id, selected.id)
                elif pos == "middle":
                    setupRepo.updateCardSlot2(player_id, selected.id)
                else:
                    setupRepo.updateCardSlot3(player_id, selected.id)

                await interaction.followup.send(
                    t(
                        guild_id,
                        "setcard.success",
                        cardName=selected.template.name,
                        cardLevel=selected.level,
                        pos=pos
                    )
                )

        except Exception as e:
            await interaction.followup.send(
                t(guild_id, "setcard.error", error=str(e)),
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(SetCard(bot))
