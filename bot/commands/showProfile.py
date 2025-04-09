import discord
from discord.ext import commands
from discord import app_commands

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.config.config import NONE_CARD_IMAGE_URL, NONE_WEAPON_IMAGE_URL
from bot.config.imageMap import CARD_IMAGE_MAP, WEAPON_IMAGE_MAP

class ShowProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="showprofile", description="Hiển thị hồ sơ chiến đấu của bạn")
    async def showProfile(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        playerId = interaction.user.id

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                playerCardRepo = PlayerCardRepository(session)
                playerWeaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)

                # Lấy thông tin người chơi
                player = playerRepo.getById(playerId)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                # Lấy thông tin active setup của người chơi
                activeSetup = activeSetupRepo.getByPlayerId(playerId)

                # Nếu chưa lắp thẻ chính (có thể đã set vũ khí)
                if not activeSetup or activeSetup.active_card_id is None:
                    if activeSetup and activeSetup.weapon_slot1 is not None:
                        activeWeapon = playerWeaponRepo.getById(activeSetup.weapon_slot1)
                        weaponImageUrl = WEAPON_IMAGE_MAP.get(activeWeapon.template.image_url, NONE_WEAPON_IMAGE_URL) if activeWeapon else NONE_WEAPON_IMAGE_URL
                    else:
                        weaponImageUrl = NONE_WEAPON_IMAGE_URL

                    embed = discord.Embed(
                        title="Hồ sơ Chiến Đấu của bạn",
                        color=discord.Color.gold()
                    )
                    embed.description = (
                        "⚠️ Bạn chưa lắp thẻ chiến đấu!\n"
                        "➜ Dùng lệnh `/setcard card: tên_thẻ` để lắp thẻ."
                    )
                    embed.set_image(url=NONE_CARD_IMAGE_URL)
                    embed.set_thumbnail(url=weaponImageUrl)
                    embed.set_footer(text=f"Số dư: {player.coin_balance:,} Ryo | Điểm rank: {player.rank_points}")
                    await interaction.followup.send(embed=embed)
                    return

                # Nếu đã lắp thẻ chính, tiến hành lấy thông tin thẻ và vũ khí
                activeCard = playerCardRepo.getById(activeSetup.active_card_id)
                activeWeapon = None
                if activeSetup.weapon_slot1 is not None:
                    activeWeapon = playerWeaponRepo.getById(activeSetup.weapon_slot1)

                # Tính sức mạnh của thẻ: sức mạnh = base_power * level
                try:
                    cardStrength = activeCard.template.base_power * activeCard.level
                except Exception:
                    cardStrength = 0

                # Xử lý thông tin vũ khí
                weaponStrength = 0
                weaponImageUrl = NONE_WEAPON_IMAGE_URL  # mặc định khi chưa set vũ khí
                if activeWeapon:
                    try:
                        weaponStrength = activeWeapon.template.bonus_power * activeWeapon.level
                    except Exception:
                        weaponStrength = 0
                    weaponImageUrl = WEAPON_IMAGE_MAP.get(activeWeapon.template.image_url, NONE_WEAPON_IMAGE_URL)

                totalStrength = cardStrength + weaponStrength
                cardImageUrl = CARD_IMAGE_MAP.get(activeCard.template.image_url, NONE_CARD_IMAGE_URL)

                # Xây dựng mô tả chi tiết theo dạng danh sách
                description_lines = [
                    f"**Tên thẻ:** {activeCard.template.name}",
                    f"**Bậc thẻ:** {activeCard.template.tier}",
                    f"**Hệ:** {activeCard.template.element}",
                    f"**Cấp thẻ:** {activeCard.level}",
                    "",
                ]
                if activeWeapon:
                    description_lines.extend([
                        f"**Tên vũ khí:** {activeWeapon.template.name}",
                        f"**Bậc vũ khí:** {activeWeapon.template.grade}",
                        f"**Cấp vũ khí:** {activeWeapon.level}",
                        "",
                    ])
                else:
                    description_lines.append("**Vũ khí:** Chưa cài đặt\n")
                description_lines.append(f"**Tổng Sức Mạnh:** {totalStrength}")

                embed = discord.Embed(
                    title="Hồ sơ Chiến Đấu của bạn",
                    description="\n".join(description_lines),
                    color=discord.Color.gold()
                )
                embed.set_image(url=cardImageUrl)
                embed.set_thumbnail(url=weaponImageUrl)
                embed.set_footer(text=f"Số dư: {player.coin_balance:,} Ryo | Điểm rank: {player.rank_points}")
                
                await interaction.followup.send(embed=embed)
        except Exception as e:
            print("❌ Lỗi khi xử lý ShowProfile:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(ShowProfile(bot))
