import discord
from discord.ext import commands
from discord import app_commands
import traceback

from bot.config.database import getDbSession
from bot.config.imageMap import WEAPON_IMAGE_MAP
from bot.config.weaponSkill import WEAPON_SKILL_MAP
from bot.repository.weaponTemplateRepository import WeaponTemplateRepository
from bot.services.i18n import t


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
        guild_id = interaction.guild.id if interaction.guild else None

        try:
            with getDbSession() as session:
                repo = WeaponTemplateRepository(session)
                weapon = repo.getByName(weapon_name)

                if not weapon:
                    await interaction.followup.send(
                        t(guild_id, "showweapon.not_found", weaponName=weapon_name),
                        ephemeral=True
                    )
                    return

                image_url = WEAPON_IMAGE_MAP.get(weapon.image_url, weapon.image_url)

                skill_key = f"weapon_skill.{weapon.image_url}"
                skill_desc = t(guild_id, skill_key)
                if skill_desc == skill_key:
                    skill_desc = WEAPON_SKILL_MAP.get(
                        weapon.image_url,
                        t(guild_id, "showweapon.skill_missing")
                    )

                crit_rate_text = f"{(weapon.bonus_crit_rate or 0):.0%}"
                dodge_text = f"{(weapon.bonus_speed or 0):.0%}"
                sell_price_text = f"{weapon.sell_price:,}"

                desc_lines = [
                    t(guild_id, "showweapon.stats.bonus_damage", value=weapon.bonus_damage or 0),
                    t(guild_id, "showweapon.stats.bonus_hp", value=weapon.bonus_health or 0),
                    t(guild_id, "showweapon.stats.bonus_armor", value=weapon.bonus_armor or 0),
                    t(guild_id, "showweapon.stats.bonus_crit_rate", value=crit_rate_text),
                    t(guild_id, "showweapon.stats.bonus_dodge", value=dodge_text),
                    t(guild_id, "showweapon.stats.bonus_chakra", value=weapon.bonus_chakra or 0),
                    t(guild_id, "showweapon.stats.grade", value=weapon.grade),
                    t(guild_id, "showweapon.stats.sell_price", value=sell_price_text),
                    "",
                    t(guild_id, "showweapon.section.skill_title"),
                    skill_desc
                ]

                embed = discord.Embed(
                    title=t(guild_id, "showweapon.title", weaponName=weapon.name),
                    description="\n".join(desc_lines),
                    color=discord.Color.gold()
                )
                embed.set_image(url=image_url)

                await interaction.followup.send(embed=embed)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(
                t(guild_id, "showweapon.error", error=tb),
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(ShowWeapon(bot))
