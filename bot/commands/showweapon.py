import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.config.imageMap import WEAPON_IMAGE_MAP
from bot.config.weaponSkill import WEAPON_SKILL_MAP
from bot.entity.weaponTemplate import WeaponTemplate

class ShowWeapon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="showweapon",
        description="Hiển thị thông tin chi tiết của một vũ khí theo tên"
    )
    @app_commands.describe(
        weapon_name="Tên của vũ khí (ví dụ: Kunai, Katana,…)"
    )
    async def showweapon(self, interaction: discord.Interaction, weapon_name: str):
        await interaction.response.defer(thinking=True)
        try:
            with getDbSession() as session:
                # Tìm vũ khí theo tên
                weapon = session.query(WeaponTemplate).filter_by(name=weapon_name).first()
                if not weapon:
                    await interaction.followup.send(
                        f"❌ Không tìm thấy vũ khí với tên `{weapon_name}`.",
                        ephemeral=True
                    )
                    return

                # Lấy URL ảnh và mô tả kỹ năng
                image_url = WEAPON_IMAGE_MAP.get(weapon.image_url, weapon.image_url)
                skill_desc = WEAPON_SKILL_MAP.get(weapon.image_url, "Chưa có kỹ năng đặc biệt.")

                # Tạo embed hiển thị thông tin vũ khí
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
                        f"**Giá bán:** {weapon.sell_price:,} Ryo\n\n\n\n"
                        f"📜 **Kỹ năng vũ khí:**\n{skill_desc}"
                    ),
                    color=discord.Color.gold()
                )
                embed.set_image(url=image_url)
                await interaction.followup.send(embed=embed)
        except Exception as e:
            print("❌ Lỗi khi xử lý showweapon:", e)
            await interaction.followup.send(
                "❌ Có lỗi xảy ra khi hiển thị vũ khí. Vui lòng thử lại sau.",
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(ShowWeapon(bot))
