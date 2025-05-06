import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.config.imageMap import CARD_IMAGE_MAP
from bot.config.characterSkill import SKILL_MAP
from bot.entity.cardTemplate import CardTemplate


class ShowCard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="showcard",
        description="Hiển thị thông tin chi tiết của một thẻ theo tên"
    )
    @app_commands.describe(
        card_name="Tên của thẻ (ví dụ: Uzumaki Naruto, Sasori, …)"
    )
    async def showcard(self, interaction: discord.Interaction, card_name: str):
        await interaction.response.defer(thinking=True)

        try:
            with getDbSession() as session:
                # Tìm theo name
                card = session.query(CardTemplate).filter_by(name=card_name).first()
                if not card:
                    await interaction.followup.send(
                        f"❌ Không tìm thấy thẻ với tên `{card_name}`.",
                        ephemeral=True
                    )
                    return

                # Lấy URL ảnh và skill description
                image_url = CARD_IMAGE_MAP.get(card.image_url, card.image_url)
                skill_desc = SKILL_MAP.get(card.image_url, "Chưa có skill đặc biệt.")

                # Tạo embed
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
                        f"**Giá bán:** {card.sell_price:,} Ryo\n\n\n\n"
                        f"📜 **Skill đặc biệt:**\n{skill_desc}"
                    ),
                    color=discord.Color.blue()
                )
                embed.set_image(url=image_url)

                await interaction.followup.send(embed=embed)
        except Exception as e:
            print("❌ Lỗi khi xử lý showcard:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra khi hiển thị thẻ. Vui lòng thử lại sau.",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(ShowCard(bot))
