import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.entity.playerCards import PlayerCard
from bot.services.i18n import t


class LevelUpCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="levelupcard",
        description="Upgrade card"
    )
    @app_commands.describe(
        card_id="card_id"
    )
    async def levelUp(self, interaction: discord.Interaction, card_id: int):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)

                # check registered
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send(f"⚠️ {t(guild_id, 'levelupcard.error.not_registered')}")
                    return

                # get card by id & ownership
                mainCardCandidate = cardRepo.getById(card_id)
                if not mainCardCandidate or mainCardCandidate.player_id != playerId:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'levelupcard.error.not_owner', card_id=card_id)}"
                    )
                    return

                card_name = mainCardCandidate.template.name
                current_level = mainCardCandidate.level
                desired_level = current_level + 1

                # max level
                if desired_level > 50:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'levelupcard.error.max_level', current_level=current_level)}"
                    )
                    return

                # get all same card_key
                cards = cardRepo.getByPlayerIdAndCardKey(playerId, mainCardCandidate.card_key)
                if not cards:
                    await interaction.followup.send(f"⚠️ {t(guild_id, 'levelupcard.error.invalid_data')}")
                    return

                # only upgrade from highest level
                highestLevel = max(c.level for c in cards)
                if highestLevel != current_level:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'levelupcard.error.not_highest_level', card_id=card_id, current_level=current_level, highest_level=highestLevel)}"
                    )
                    return

                # cannot upgrade if equipped
                if mainCardCandidate.equipped:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'levelupcard.error.equipped', card_name=card_name, card_id=mainCardCandidate.id)}"
                    )
                    return

                # materials (level 1) = 3 * current_level
                requiredMaterials = 3 * current_level
                level1Cards = [c for c in cards if c.level == 1]
                totalLevel1Quantity = sum(c.quantity for c in level1Cards)

                if totalLevel1Quantity < requiredMaterials:
                    await interaction.followup.send(
                        f"⚠️ {t(guild_id, 'levelupcard.error.not_enough_materials', card_name=card_name, required=requiredMaterials, current=totalLevel1Quantity)}"
                    )
                    return

                #  consume main card (1 copy)
                if mainCardCandidate.quantity > 1:
                    mainCardCandidate.quantity -= 1
                else:
                    cardRepo.deleteCard(mainCardCandidate)

                # create upgraded card record
                newCard = PlayerCard(
                    player_id=playerId,
                    card_key=mainCardCandidate.card_key,
                    level=desired_level,
                    quantity=1,
                    equipped=False,
                    locked=mainCardCandidate.locked
                )
                cardRepo.create(newCard)

                # consume level 1 materials
                remaining = requiredMaterials
                for c in level1Cards:
                    if remaining <= 0:
                        break
                    if c.quantity <= remaining:
                        remaining -= c.quantity
                        cardRepo.deleteCard(c)
                    else:
                        c.quantity -= remaining
                        if c.quantity == 0:
                            cardRepo.deleteCard(c)
                        remaining = 0

                # exp reward
                playerRepo.incrementExp(playerId, amount=5)

                session.commit()

                await interaction.followup.send(
                    f"✅ {t(guild_id, 'levelupcard.success', card_name=card_name, new_card_id=newCard.id, from_level=current_level, to_level=desired_level)}"
                )

        except Exception as e:
            print("❌ Lỗi khi xử lý levelup:", e)
            await interaction.followup.send(f"❌ {t(guild_id, 'levelupcard.error.generic')}")


async def setup(bot):
    await bot.add_cog(LevelUpCard(bot))
