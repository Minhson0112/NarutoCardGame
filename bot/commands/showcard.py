import discord
from discord.ext import commands
from discord import app_commands
import traceback

from bot.config.database import getDbSession
from bot.config.imageMap import CARD_IMAGE_MAP
from bot.config.characterSkill import SKILL_MAP
from bot.repository.cardTemplateRepository import CardTemplateRepository


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

        try:
            with getDbSession() as session:
                repo = CardTemplateRepository(session)
                card = repo.getByName(card_name)

                if not card:
                    await interaction.followup.send(
                        f"❌ Không tìm thấy thẻ với tên `{card_name}`.",
                        ephemeral=True
                    )
                    return

                image_url = CARD_IMAGE_MAP.get(card.image_url, card.image_url)
                skill_desc = SKILL_MAP.get(card.image_url, "Chưa có skill đặc biệt.")

                embed = discord.Embed(
                    title=f"🔍 Thẻ: {card.name}",
                    description=(
                        f"**Damage:** {card.base_damage}\n"
                        f"**Hp:** {card.health}\n"
                        f"**Giáp:** {card.armor}\n"
                        f"**Tỉ lệ chí mạng:** {card.crit_rate:.0%}\n"
                        f"**Né:** {card.speed:.0%}\n"
                        f"**Chakra gốc:** {card.chakra}\n"
                        f"**Tanker:** {'✅' if card.first_position else '❌'}\n"
                        f"**Bậc:** {card.tier}\n"
                        f"**Hệ chakra:** {card.element}\n"
                        f"**Giá bán:** {card.sell_price:,} Ryo\n\n"
                        f"📜 **Skill đặc biệt:**\n{skill_desc}"
                    ),
                    color=discord.Color.blue()
                )
                embed.set_image(url=image_url)

                await interaction.followup.send(embed=embed)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(f"❌ Có lỗi xảy ra:\n```{tb}```", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(ShowCard(bot))
