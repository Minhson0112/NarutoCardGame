import discord
from discord.ext import commands
from discord import app_commands
import random

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.config.config import VS_IMAGE, NONE_CARD_IMAGE_URL, NONE_WEAPON_IMAGE_URL, ELEMENT_COUNTER
from bot.config.imageMap import CARD_IMAGE_MAP, WEAPON_IMAGE_MAP
from bot.entity.player import Player  # model Player

class Fight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fight", description="Thách đấu người chơi cùng trình độ")
    async def fight(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        attacker_id = interaction.user.id

        try:
            with getDbSession() as session:
                # Lấy các repository cần thiết
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)
                
                # Lấy thông tin người tấn công
                attacker = playerRepo.getById(attacker_id)
                if not attacker:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return
                
                # Lấy active setup của người tấn công
                attackerSetup = activeSetupRepo.getByPlayerId(attacker_id)
                if not attackerSetup or attackerSetup.active_card_id is None:
                    await interaction.followup.send("⚠️ Bạn chưa lắp thẻ chiến đấu. Hãy dùng /setcard trước khi đấu.")
                    return
                attackerCard = cardRepo.getById(attackerSetup.active_card_id)
                attackerWeapon = None
                if attackerSetup.weapon_slot1 is not None:
                    attackerWeapon = weaponRepo.getById(attackerSetup.weapon_slot1)
                
                # Tính sức mạnh của người tấn công
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
                
                # Tìm các đối thủ có rank_points trong khoảng [attacker.rank_points - 50, attacker.rank_points + 50] (ngoại trừ attacker)
                minRank = attacker.rank_points - 50
                maxRank = attacker.rank_points + 50
                opponents = session.query(Player).filter(
                    Player.player_id != attacker_id,
                    Player.rank_points >= minRank,
                    Player.rank_points <= maxRank
                ).all()
                
                # Lọc lại chỉ những người đã lắp thẻ (active_setup tồn tại và active_card_id không null)
                valid_opponents = []
                for opp in opponents:
                    oppSetup = activeSetupRepo.getByPlayerId(opp.player_id)
                    if oppSetup and oppSetup.active_card_id is not None:
                        valid_opponents.append(opp)
                        
                if not valid_opponents:
                    await interaction.followup.send("⚠️ Chưa tìm thấy đối thủ cùng trình độ với bạn.")
                    return
                
                defender = random.choice(valid_opponents)
                
                # Lấy active setup của đối thủ
                defenderSetup = activeSetupRepo.getByPlayerId(defender.player_id)
                defenderCard = cardRepo.getById(defenderSetup.active_card_id)
                defenderWeapon = None
                if defenderSetup.weapon_slot1 is not None:
                    defenderWeapon = weaponRepo.getById(defenderSetup.weapon_slot1)
                
                # Tính sức mạnh của đối thủ
                try:
                    defenderCardStrength = defenderCard.template.base_power * defenderCard.level
                except Exception:
                    defenderCardStrength = 0
                defenderWeaponStrength = 0
                if defenderWeapon:
                    try:
                        defenderWeaponStrength = defenderWeapon.template.bonus_power * defenderWeapon.level
                    except Exception:
                        defenderWeaponStrength = 0
                defenderTotalStrength = defenderCardStrength + defenderWeaponStrength
                
                # Xác định kết quả trận đấu (chỉ cập nhật attacker)
                bonus_reward = 0  # số tiền thưởng dựa trên việc đánh bại đối thủ
                bonus_highest = 0 # thưởng khi đạt được thành tích cao mới
                counterMsg = ""
                # tính ngũ hành 
                attacker_element = attackerCard.template.element
                defender_element = defenderCard.template.element
                if attacker_element != "Thể" and defender_element != "Thể":
                    if ELEMENT_COUNTER.get(attacker_element) == defender_element:
                        defenderTotalStrength += 50
                        counterMsg = f"**Thuộc tính chakra:** Vì {defender_element} khắc {attacker_element} nên {defender.username} nhận thêm 50 điểm sức mạnh"
                    elif ELEMENT_COUNTER.get(defender_element) == attacker_element:
                        attackerTotalStrength += 50
                        counterMsg = f"**Thuộc tính chakra:** Vì {attacker_element} khắc {defender_element} nên {attacker.username} nhận thêm 50 điểm sức mạnh"
                    else:
                        counterMsg = f"**Thuộc tính chakra:** {attacker_element} và {defender_element} Không tương khắc, không ai được nhận thêm sức mạnh"
                else:
                    counterMsg = f"**Thuộc tính chakra:** Thể thuật không có tương sinh tương khắc, không ai được nhận thêm sức mạnh"
                        
                if attackerTotalStrength > defenderTotalStrength:
                    result = "win"
                    attacker.rank_points += 5
                    attacker.winning_streak += 1
                    # Thưởng theo chuỗi thắng: 500 ryo * winning_streak
                    bonus_reward = 500 * attacker.winning_streak
                    # Kiểm tra thành tích cao mới
                    if attacker.rank_points > attacker.highest_rank_points:
                        bonus_highest = 5000
                        attacker.highest_rank_points = attacker.rank_points
                elif attackerTotalStrength < defenderTotalStrength:
                    result = "loss"
                    attacker.rank_points = max(0, attacker.rank_points - 5)
                    attacker.winning_streak = 0
                else:
                    result = "draw"
                    attacker.winning_streak = 0
                
                # Cộng thưởng vào số dư coin của attacker (nếu thắng)
                if result == "win":
                    attacker.coin_balance += bonus_reward + bonus_highest
                
                session.commit()
                
                # Xây dựng embed thông tin người tấn công theo dạng danh sách
                attackerCardInfo = (
                    f"•🥷 **Tên thẻ:** {attackerCard.template.name}\n"
                    f"  ┣ **Bậc:** {attackerCard.template.tier}\n"
                    f"  ┣ **Hệ:** {attackerCard.template.element}\n"
                    f"  ┗ **Level:** {attackerCard.level}"
                )
                if attackerWeapon:
                    attackerWeaponInfo = (
                        f"•🔪 **Tên vũ khí:** {attackerWeapon.template.name}\n"
                        f"  ┣ **Bậc:** {attackerWeapon.template.grade}\n"
                        f"  ┗ **Level:** {attackerWeapon.level}"
                    )
                else:
                    attackerWeaponInfo = "• **Vũ khí:** Chưa cài đặt"
                attackerDescription = (
                    f"**Thông tin Thẻ Chiến Đấu:**\n{attackerCardInfo}\n\n"
                    f"**Thông tin Vũ Khí:**\n{attackerWeaponInfo}\n\n"
                    f"**Tổng Sức Mạnh:** {attackerTotalStrength}"
                )
                embed_attacker = discord.Embed(
                    title=f"Người tấn công: {attacker.username}",
                    description=attackerDescription,
                    color=discord.Color.gold()
                )
                embed_attacker.set_image(url=CARD_IMAGE_MAP.get(attackerCard.template.image_url, NONE_CARD_IMAGE_URL))
                embed_attacker.set_thumbnail(url=WEAPON_IMAGE_MAP.get(attackerWeapon.template.image_url, NONE_WEAPON_IMAGE_URL) if attackerWeapon else NONE_WEAPON_IMAGE_URL)
                embed_attacker.set_footer(text=f"Điểm rank: {attacker.rank_points}")
                
                # Embed VS: sử dụng hình ảnh từ VS_IMAGE
                embed_vs = discord.Embed(color=discord.Color.dark_red())
                embed_vs.set_image(url=VS_IMAGE)
                
                # Xây dựng embed thông tin người bị tấn công theo dạng danh sách
                defenderCardInfo = (
                    f"•🥷 **Tên thẻ:** {defenderCard.template.name}\n"
                    f"  ┣ **Bậc:** {defenderCard.template.tier}\n"
                    f"  ┣ **Hệ:** {defenderCard.template.element}\n"
                    f"  ┗ **Level:** {defenderCard.level}"
                )
                if defenderWeapon:
                    defenderWeaponInfo = (
                        f"•🔪 **Tên vũ khí:** {defenderWeapon.template.name}\n"
                        f"  ┣ **Bậc:** {defenderWeapon.template.grade}\n"
                        f"  ┗ **Level:** {defenderWeapon.level}"
                    )
                else:
                    defenderWeaponInfo = "• **Vũ khí:** Chưa cài đặt"
                defenderDescription = (
                    f"**Thông tin Thẻ Chiến Đấu:**\n{defenderCardInfo}\n\n"
                    f"**Thông tin Vũ Khí:**\n{defenderWeaponInfo}\n\n"
                    f"**Tổng Sức Mạnh:** {defenderTotalStrength}"
                )
                embed_defender = discord.Embed(
                    title=f"Người bị tấn công: {defender.username}",
                    description=defenderDescription,
                    color=discord.Color.gold()
                )
                embed_defender.set_image(url=CARD_IMAGE_MAP.get(defenderCard.template.image_url, NONE_CARD_IMAGE_URL))
                embed_defender.set_thumbnail(url=WEAPON_IMAGE_MAP.get(defenderWeapon.template.image_url, NONE_WEAPON_IMAGE_URL) if defenderWeapon else NONE_WEAPON_IMAGE_URL)
                embed_defender.set_footer(text=f"Điểm rank: {defender.rank_points}")
                
                # Tạo embed kết quả trận đấu
                if result == "win":
                    outcome_text = f"Người tấn công (**{attacker.username}**) chiến thắng! (+5 điểm rank)\n\n"
                elif result == "loss":
                    outcome_text = f"Người tấn công (**{attacker.username}**) thất bại! (-5 điểm rank)\n\n"
                else:
                    outcome_text = "Trận đấu hòa!"
                embed_result = discord.Embed(
                    title="Kết quả Trận Chiến",
                    description=(
                        f"{counterMsg}\n\n"
                        f"**Kết quả:** {result.upper()}\n"
                        f"Người tấn công (**{attacker.username}**): **{attackerTotalStrength}**\n"
                        f"Người bị tấn công (**{defender.username}**): **{defenderTotalStrength}**\n\n"
                        f"{outcome_text}\n"
                        f"**Thưởng:** {bonus_reward + bonus_highest:,} Ryo\n"
                        f"**Chuỗi thắng:** {attacker.winning_streak}"
                    ),
                    color=discord.Color.green() if result == "win" else discord.Color.red() if result == "loss" else discord.Color.orange()
                )
                
                # Gửi 4 embed cùng lúc
                await interaction.followup.send(embeds=[embed_attacker, embed_vs, embed_defender, embed_result])
        except Exception as e:
            print("❌ Lỗi khi xử lý fight:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")

async def setup(bot):
    await bot.add_cog(Fight(bot))
