import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy import func

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.config.config import VS_IMAGE, NONE_CARD_IMAGE_URL, NONE_WEAPON_IMAGE_URL
from bot.config.imageMap import CARD_IMAGE_MAP, WEAPON_IMAGE_MAP, STORY_IMAGE_MAP
from bot.entity.challenge import Challenge

class ChallengeGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="challenge", description="Vượt qua thử thách để nhận thưởng")
    async def challenge(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        player_id = interaction.user.id

        try:
            with getDbSession() as session:
                # Khởi tạo các repository cần thiết
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)

                # Lấy thông tin người chơi
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                # Kiểm tra active setup của người chơi (phải đã lắp thẻ chiến đấu)
                activeSetup = activeSetupRepo.getByPlayerId(player_id)
                if not activeSetup or activeSetup.active_card_id is None:
                    await interaction.followup.send("⚠️ Bạn chưa lắp thẻ chiến đấu. Hãy dùng /setcard trước khi thử thách.")
                    return

                # Lấy thẻ chiến đấu và vũ khí của người chơi
                attackerCard = cardRepo.getById(activeSetup.active_card_id)
                attackerWeapon = None
                if activeSetup.weapon_slot1 is not None:
                    attackerWeapon = weaponRepo.getById(activeSetup.weapon_slot1)

                # Tính sức mạnh của người chơi
                try:
                    attackerCardStrength = attackerCard.template.base_power * attackerCard.level
                except Exception:
                    attackerCardStrength = 0
                attackerWeaponStrength = 0
                if attackerWeapon:
                    try:
                        attackerWeaponStrength = attackerWeapon.template.bonus_power * attackerWeapon.level
                    except Exception:
                        attackerWeaponStrength = 0
                attackerTotalStrength = attackerCardStrength + attackerWeaponStrength

                # Xác định challenge hiện tại của người chơi:
                # Nếu player.challenge_id là null thì currentChallengeId = 1; ngược lại, dùng giá trị của player.challenge_id.
                currentChallengeId = player.challenge_id if player.challenge_id is not None else 1

                # Lấy thử thách (challenge) dựa trên currentChallengeId
                challenge = session.query(Challenge).filter_by(id=currentChallengeId).first()
                if not challenge:
                    await interaction.followup.send("⚠️ Không tìm thấy thử thách cho ID này. Vui lòng liên hệ admin.")
                    return

                # Sử dụng STORY_IMAGE_MAP để lấy URL ảnh dựa trên challenge.image_url_key
                challengeImageUrl = STORY_IMAGE_MAP.get(challenge.image_url_key, NONE_CARD_IMAGE_URL)

                # So sánh sức mạnh: nếu attackerTotalStrength > challenge.card_strength => thắng;
                # nếu attackerTotalStrength <= challenge.card_strength => thua (không mất gì)
                if attackerTotalStrength > challenge.card_strength:
                    result = "win"
                    outcome_text = (
                        f"🥳 Chúc mừng! Bạn đã vượt qua thử thách **{challenge.card_name}**.\n"
                        f"Nhận thưởng: **{challenge.bonus_ryo} Ryo**!"
                    )
                    # Cộng thưởng bonus_ryo vào số dư
                    player.coin_balance += challenge.bonus_ryo
                    # Cập nhật challenge_id: nếu ban đầu là null thì đặt thành 2; nếu không thì tăng thêm 1
                    if player.challenge_id is None:
                        player.challenge_id = 2
                    else:
                        player.challenge_id += 1

                    # Kiểm tra xem player.challenge_id có vượt quá max challenge hiện có hay không
                    maxChallengeId = 32
                    if player.challenge_id == maxChallengeId:
                        outcome_text += "\n\n🎉 Bạn đã vượt qua hết các thử thách hiện có. Chúng tôi sẽ cập nhật thêm thử thách mới trong tương lai!"
                else:
                    result = "loss"
                    outcome_text = (
                        f"😢 Rất tiếc! Bạn không vượt qua thử thách **{challenge.card_name}**.\n"
                        f"Bạn không nhận được thưởng."
                    )
                    # Nếu thua, không cập nhật số dư hay challenge_id

                session.commit()

                # --- Embed thông tin người tấn công (Embed 1) ---
                attackerCardInfo = (
                    f"• 🥷 **Tên thẻ:** {attackerCard.template.name}\n"
                    f"  ┣ **Bậc:** {attackerCard.template.tier}\n"
                    f"  ┣ **Hệ:** {attackerCard.template.element}\n"
                    f"  ┗ **Level:** {attackerCard.level}"
                )
                if attackerWeapon:
                    attackerWeaponInfo = (
                        f"• 🔪 **Tên vũ khí:** {attackerWeapon.template.name}\n"
                        f"  ┣ **Bậc:** {attackerWeapon.template.grade}\n"
                        f"  ┗ **Level:** {attackerWeapon.level}"
                    )
                else:
                    attackerWeaponInfo = "• 🔪 **Vũ khí:** Chưa cài đặt"
                attackerDescription = (
                    f"**Thông tin Thẻ Chiến Đấu:**\n{attackerCardInfo}\n\n"
                    f"**Thông tin Vũ Khí:**\n{attackerWeaponInfo}\n\n"
                    f"**Tổng Sức Mạnh:** {attackerTotalStrength}"
                )
                embedAttacker = discord.Embed(
                    title=f"Tham gia thử thách: {player.username}",
                    description=attackerDescription,
                    color=discord.Color.gold()
                )
                # Hiển thị ảnh thẻ ở phần image
                embedAttacker.set_image(url=CARD_IMAGE_MAP.get(attackerCard.template.image_url, NONE_CARD_IMAGE_URL))
                # Hiển thị ảnh vũ khí ở phần thumbnail (nếu có)
                if attackerWeapon:
                    embedAttacker.set_thumbnail(url=WEAPON_IMAGE_MAP.get(attackerWeapon.template.image_url, NONE_WEAPON_IMAGE_URL))
                else:
                    embedAttacker.set_thumbnail(url=NONE_WEAPON_IMAGE_URL)
                embedAttacker.set_footer(text=f"Điểm rank: {player.rank_points}")

                # --- Embed VS (Embed 2) ---
                embedVs = discord.Embed(color=discord.Color.dark_red())
                embedVs.set_image(url=VS_IMAGE)

                # --- Embed thông tin thử thách (Embed 3) ---
                challengeDescription = (
                    f"**Nội dung:** {challenge.narrative}\n\n"
                    f"**Sức Mạnh Thử Thách:** {challenge.card_strength}\n"
                    f"**Tiền thưởng:** {challenge.bonus_ryo} Ryo"
                )
                embedChallenge = discord.Embed(
                    title=f"**Tên thử thách:** {challenge.card_name}",
                    description=challengeDescription,
                    color=discord.Color.purple()
                )
                embedChallenge.set_image(url=challengeImageUrl)
                embedChallenge.set_footer(text=f"Thử thách hiện tại của bạn: {currentChallengeId}")

                # --- Embed kết quả (Embed 4) ---
                finalColor = discord.Color.green() if result == "win" else discord.Color.red()
                embedResult = discord.Embed(
                    title="Kết quả Thử Thách",
                    description=(
                        f"**Kết quả:** {result.upper()}\n"
                        f"Sức mạnh của bạn: **{attackerTotalStrength}**\n"
                        f"Sức mạnh thử thách: **{challenge.card_strength}**\n\n"
                        f"{outcome_text}"
                    ),
                    color=finalColor
                )

                # Gửi 4 Embed cùng lúc bằng followup.send (vì interaction đã được defer)
                await interaction.followup.send(embeds=[embedAttacker, embedVs, embedChallenge, embedResult])
        except Exception as e:
            print("❌ Lỗi khi xử lý /challenge:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ChallengeGame(bot))
