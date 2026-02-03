import discord
from discord.ext import commands
from discord import app_commands
import traceback

from bot.config.database import getDbSession
from bot.config.imageMap import WEAPON_IMAGE_MAP
from bot.config.weaponSkill import WEAPON_SKILL_MAP
from bot.repository.weaponTemplateRepository import WeaponTemplateRepository


class ShowWeapon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def weaponNameAutocomplete(self, interaction: discord.Interaction, current: str):
        typed = (current or "").strip()
        if not typed:
            return []

        try:
            with getDbSession() as session:
                repo = WeaponTemplateRepository(session)
                names = repo.searchNamesForAutocomplete(typed, limit=25)
                return [app_commands.Choice(name=n, value=n) for n in names]
        except Exception:
            return []

    @app_commands.command(
        name="showweapon",
        description="Hiển thị thông tin chi tiết của một vũ khí theo tên"
    )
    @app_commands.describe(weapon_name="Gõ vài chữ để hiện gợi ý")
    @app_commands.autocomplete(weapon_name=weaponNameAutocomplete)
    async def showweapon(self, interaction: discord.Interaction, weapon_name: str):
        await interaction.response.defer(thinking=True)

        try:
            with getDbSession() as session:
                repo = WeaponTemplateRepository(session)
                weapon = repo.getByName(weapon_name)

                if not weapon:
                    await interaction.followup.send(
                        f"❌ Không tìm thấy vũ khí với tên `{weapon_name}`.",
                        ephemeral=True
                    )
                    return

                image_url = WEAPON_IMAGE_MAP.get(weapon.image_url, weapon.image_url)
                skill_desc = WEAPON_SKILL_MAP.get(weapon.image_url, "Chưa có kỹ năng đặc biệt.")

                embed = discord.Embed(
                    title=f"🔨 Vũ khí: {weapon.name}",
                    description=(
                        f"**Damage cộng thêm:** {weapon.bonus_damage or 0}\n"
                        f"**Hp cộng thêm:** {weapon.bonus_health or 0}\n"
                        f"**Giáp cộng thêm:** {weapon.bonus_armor or 0}\n"
                        f"**Tỉ lệ chí mạng cộng thêm:** {(weapon.bonus_crit_rate or 0):.0%}\n"
                        f"**Né cộng thêm:** {(weapon.bonus_speed or 0):.0%}\n"
                        f"**Chakra cộng thêm:** {weapon.bonus_chakra or 0}\n"
                        f"**Bậc:** {weapon.grade}\n"
                        f"**Giá bán:** {weapon.sell_price:,} Ryo\n\n"
                        f"📜 **Kỹ năng vũ khí:**\n{skill_desc}"
                    ),
                    color=discord.Color.gold()
                )
                embed.set_image(url=image_url)

                await interaction.followup.send(embed=embed)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(f"❌ Có lỗi xảy ra:\n```{tb}```", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(ShowWeapon(bot))
