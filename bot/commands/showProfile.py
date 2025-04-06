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

                # Nếu chưa lắp thẻ chính, nhưng có thể đã set vũ khí
                if not activeSetup or activeSetup.active_card_id is None:
                    # Nếu đã set vũ khí thì lấy ảnh vũ khí, nếu không thì dùng ảnh mặc định
                    if activeSetup and activeSetup.weapon_slot1 is not None:
                        activeWeapon = playerWeaponRepo.getById(activeSetup.weapon_slot1)
                        weaponImageUrl = WEAPON_IMAGE_MAP.get(activeWeapon.template.image_url, NONE_WEAPON_IMAGE_URL) if activeWeapon else NONE_WEAPON_IMAGE_URL
                    else:
                        weaponImageUrl = NONE_WEAPON_IMAGE_URL

                    embed = discord.Embed(
                        title="Hồ sơ chiến đấu của bạn",
                        color=discord.Color.gold()
                    )
                    embed.add_field(
                        name="Thông báo",
                        value="⚠️ Bạn chưa lắp thẻ chiến đấu. Dùng lệnh /setcard card: tên_thẻ để lắp thẻ.",
                        inline=False
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

                # Lấy ảnh thẻ: sử dụng key từ activeCard.template.image_url với CARD_IMAGE_MAP
                cardImageUrl = CARD_IMAGE_MAP.get(activeCard.template.image_url, NONE_CARD_IMAGE_URL)

                # Tạo embed với thông tin thẻ chiến đấu
                embed = discord.Embed(
                    title="Hồ sơ chiến đấu của bạn",
                    description="Đây là thẻ chiến đấu của bạn:",
                    color=discord.Color.gold()
                )
                embed.add_field(name="Tên thẻ", value=f"**{activeCard.template.name}**", inline=True)
                embed.add_field(name="Bậc thẻ", value=f"**{activeCard.template.tier}**", inline=True)
                embed.add_field(name="Cấp thẻ", value=f"**{activeCard.level}**", inline=True)

                # Nếu có thông tin vũ khí thì thêm các trường chi tiết của vũ khí
                if activeWeapon:
                    embed.add_field(name="Tên vũ khí", value=f"**{activeWeapon.template.name}**", inline=True)
                    embed.add_field(name="Bậc vũ khí", value=f"**{activeWeapon.template.grade}**", inline=True)
                    embed.add_field(name="Cấp vũ khí", value=f"**{activeWeapon.level}**", inline=True)
                else:
                    embed.add_field(name="Vũ khí", value="Chưa cài đặt", inline=False)

                embed.add_field(name="Tổng Sức Mạnh:", value=f"**{totalStrength}**", inline=True)
                embed.set_image(url=cardImageUrl)
                embed.set_thumbnail(url=weaponImageUrl)
                embed.set_footer(text=f"Số dư: {player.coin_balance:,} Ryo | Điểm rank: {player.rank_points}")

                await interaction.followup.send(embed=embed)
        except Exception as e:
            print("❌ Lỗi khi xử lý ShowProfile:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(ShowProfile(bot))
