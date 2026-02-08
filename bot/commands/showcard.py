import discord
from discord.ext import commands
from discord import app_commands
import traceback

from bot.config.database import getDbSession
from bot.config.imageMap import CARD_IMAGE_MAP
from bot.repository.cardTemplateRepository import CardTemplateRepository
from bot.services.i18n import t


class ShowCard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cardNameAutocomplete(self, interaction: discord.Interaction, current: str):
        typed = (current or "").strip()
        if not typed:
            return []

        try:
            with getDbSession() as session:
                repo = CardTemplateRepository(session)
                names = repo.searchNamesForAutocomplete(typed, limit=25)
                return [app_commands.Choice(name=n, value=n) for n in names]
        except Exception:
            return []

    @app_commands.command(
        name="showcard",
        description="Hiển thị thông tin chi tiết của một thẻ theo tên"
    )
    @app_commands.describe(card_name="Gõ vài chữ để hiện gợi ý")
    @app_commands.autocomplete(card_name=cardNameAutocomplete)
    async def showcard(self, interaction: discord.Interaction, card_name: str):
        await interaction.response.defer(thinking=True)

        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                repo = CardTemplateRepository(session)
                card = repo.getByName(card_name)

                if not card:
                    await interaction.followup.send(
                        t(guild_id, "showcard.not_found", cardName=card_name),
                        ephemeral=True
                    )
                    return

                image_url = CARD_IMAGE_MAP.get(card.image_url, card.image_url)

                skill_key = f"skill.{card.image_url}"
                skill_desc = t(guild_id, skill_key)
                if skill_desc == skill_key:
                    skill_desc = t(guild_id, "showcard.skill_missing")

                tanker_icon = t(guild_id, "common.yes_icon") if card.first_position else t(guild_id, "common.no_icon")

                crit_rate_text = f"{card.crit_rate:.0%}"
                dodge_text = f"{card.speed:.0%}"

                desc_lines = [
                    t(guild_id, "showcard.stats.damage", value=card.base_damage),
                    t(guild_id, "showcard.stats.hp", value=card.health),
                    t(guild_id, "showcard.stats.armor", value=card.armor),
                    t(guild_id, "showcard.stats.crit_rate", value=crit_rate_text),
                    t(guild_id, "showcard.stats.dodge", value=dodge_text),
                    t(guild_id, "showcard.stats.base_chakra", value=card.chakra),
                    t(guild_id, "showcard.stats.tanker", value=tanker_icon),
                    t(guild_id, "showcard.stats.tier", value=card.tier),
                    t(guild_id, "showcard.stats.element", value=card.element),
                    t(guild_id, "showcard.stats.sell_price", value=card.sell_price),
                    "",
                    t(guild_id, "showcard.skill_title"),
                    skill_desc,
                ]

                embed = discord.Embed(
                    title=t(guild_id, "showcard.title", cardName=card.name),
                    description="\n".join(desc_lines),
                    color=discord.Color.blue()
                )
                embed.set_image(url=image_url)

                await interaction.followup.send(embed=embed)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(
                t(guild_id, "showcard.error", error=tb),
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(ShowCard(bot))
