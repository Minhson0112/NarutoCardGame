import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy import func

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.config.config import VS_IMAGE, NONE_CARD_IMAGE_URL, NONE_WEAPON_IMAGE_URL
from bot.config.imageMap import CARD_IMAGE_MAP, WEAPON_IMAGE_MAP, STORY_IMAGE_MAP
from bot.entity.challenge import Challenge
from bot.services.help import get_battle_card_params
from bot.services.createCard import create_card
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
                dailyTaskRepo = DailyTaskRepository(session)

                # Lấy thông tin người chơi
                player = playerRepo.getById(player_id)
                if not player:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return

                # Lấy active setup của người tấn công
                attackerSetup = activeSetupRepo.getByPlayerId(player_id)
                # Kiểm 3 slot thẻ
                slots = [
                    attackerSetup.card_slot1,
                    attackerSetup.card_slot2,
                    attackerSetup.card_slot3,
                ]
                if any(slot is None for slot in slots):
                    await interaction.followup.send(
                        "⚠️ Bạn phải lắp đủ 3 thẻ (Tanker, Middle, Back) mới có thể tham gia đấu!"
                    )
                    return

                # Nếu đầy đủ, lấy ra các đối tượng PlayerCard
                attacker_cards = [
                    cardRepo.getById(slot_id)
                    for slot_id in slots
                ]

                # lấy vũ khí
                attacker_weapon_slots = [
                    attackerSetup.weapon_slot1,
                    attackerSetup.weapon_slot2,
                    attackerSetup.weapon_slot3,
                ]
                attacker_weapons = [
                    weaponRepo.getById(wsid) if wsid is not None else None
                    for wsid in attacker_weapon_slots
                ]

                battle_attacker_team = []
                for pc, pw in zip(attacker_cards, attacker_weapons):
                    # Lấy tuple params đã buff level + bonus vũ khí
                    params = get_battle_card_params(pc, pw)
                    # Create đúng subclass dựa trên element và tier
                    battle_card = create_card(*params)
                    battle_attacker_team.append(battle_card)

                total_damage = sum(card.base_damage for card in battle_attacker_team)
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
                if total_damage > challenge.card_strength:
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
                dailyTaskRepo.updateStageClear(player_id)

                # --- Embed thông tin người tấn công (Embed 1) ---
                initial_desc = []
                initial_desc.append("**Team tham gia thử thách**\n")
                for c in battle_attacker_team:
                    initial_desc.append(
                        f"{c.name}"
                        f"  ⚔️{c.base_damage}\n")
                embedAttacker = discord.Embed(
                    title=f"Tham gia thử thách: {player.username}",
                    description="\n".join(initial_desc),
                    color=discord.Color.gold()
                )
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
                        f"Sức mạnh của bạn: **{total_damage}**\n"
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
