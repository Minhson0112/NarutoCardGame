import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import checks, CommandOnCooldown
import random
import asyncio
import traceback

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.repository.cardTemplateRepository import CardTemplateRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.config.imageMap import CARD_IMAGE_LOCAL_PATH_MAP, BG_ADVENTURE, NON_CARD_PATH
from bot.entity.player import Player
from bot.services.fightRender import renderImageFight
from bot.services.help import get_battle_card_params
from bot.services.createCard import create_card

def get_default_target(enemy_team):
    for idx in range(3):  # hàng đầu -> giữa -> sau
        if enemy_team[idx].is_alive():
            return enemy_team[idx]
    return None

def is_team_alive(team):
    return any(card.is_alive() for card in team)

def increase_chakra(team):
    for card in team:
        if card.is_alive():
            card.chakra += 20

def get_team_total_speed(team):
    return sum(card.speed for card in team if card.is_alive())

def battle_turn(attacker_team, enemy_team):
    logs = []
    for atk in attacker_team:
        if not atk.is_alive():
            continue

        if atk.chakra >= 100:
            logs.append(f"{atk.name} dùng kỹ năng đặc biệt!")
            # giả sử special_skills() trả về list[str]
            logs += atk.special_skills()
            atk.chakra = 0
        else:
            tgt = atk.target if atk.target and atk.target.is_alive() else get_default_target(enemy_team)
            if not tgt:
                logs.append(f"{atk.name} không có mục tiêu.")
                continue

            logs.append(f"**{atk.name}** tấn công **{tgt.name}**")
            if random.random() < tgt.speed:
                logs.append(f"→ {tgt.name} né thành công! ({tgt.speed:.0%})")
            else:
                crit = random.random() < atk.crit_rate
                dmg = max(atk.base_damage * (2 if crit else 1) - tgt.armor, 0)
                tgt.health = max(tgt.health - dmg, 0)
                prefix = "💥 CHÍ MẠNG! " if crit else ""
                logs.append(f"→ {prefix}Gây {dmg} sát thương;")
        # tăng chakra mỗi lượt
        atk.chakra += 20
    return logs

class Adventure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name= "adventure", description= "đi thám hiểm, dẹp loạn, nhận ryo nếu thắng")
    @checks.cooldown(1, 300, key=lambda interaction: interaction.user.id)
    async def adventure(self, interaction: discord.Interaction):
        attacker_id = interaction.user.id
        await interaction.response.defer(thinking=True)
        
        teamNames = ["Team thích thể hiện", "Team phổi to", "Team phá làng phá xóm", "Team giang hồ mõm",
                    "Team cung bọ cạp", "Team biết bố mày là ai không", "Team chọc gậy bánh xe", "Team nghiện cờ bạc",
                    "Team con nhà người ta", "Team thì ra mày chọn cái chết", "Team mình tao chấp hết",
                    "Team tao có kiên", "Team hacker lỏ", "Team Không trượt phát lào", "Team tuổi l sánh vai", "Team đầu chộm đuôi cướp",
                    "Team buôn hàng nóng", "Team gấu tró", "Team máu dồn lên não", "Team wibu", "Team fan mu", "Team đáy xã hội", 
                    "Team phụ hồ", "Team Ca sĩ hàn quốc", "Team đom đóm", "Team hội mê peter"]
        teamName = random.choice(teamNames)
        try:
            with getDbSession() as session:
                # Lấy các repository cần thiết
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                cardtemplaterepo = CardTemplateRepository(session)
                
                # Lấy thông tin người tấn công
                attacker = playerRepo.getById(attacker_id)
                if not attacker:
                    await interaction.followup.send("⚠️ Bạn chưa đăng ký tài khoản. Hãy dùng /register trước nhé!")
                    return
                
                # Lấy active setup của người tấn công
                attackerSetup = activeSetupRepo.getByPlayerId(attacker_id)
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

                battle_defender_team = []
                defenderCardImgPaths = []
                list_card = cardtemplaterepo.getFormationTemplates()
                for card in list_card:
                    img_path = CARD_IMAGE_LOCAL_PATH_MAP.get(card.image_url, NON_CARD_PATH)
                    battle_card = create_card(card.name, card.health, card.armor, card.base_damage, card.crit_rate, card.speed, card.chakra, card.element, card.tier)
                    battle_defender_team.append(battle_card)
                    defenderCardImgPaths.append(img_path)

                attackCardImgpaths = []
                for pc in attacker_cards:
                    key = pc.template.image_url
                    # nếu không tìm thấy key trong map thì fallback sang NON_CARD_PATH nếu bạn có
                    img_path = CARD_IMAGE_LOCAL_PATH_MAP.get(key, NON_CARD_PATH)
                    attackCardImgpaths.append(img_path)

                paths = attackCardImgpaths + defenderCardImgPaths
                buffer = renderImageFight(
                    paths[0], paths[1], paths[2],
                    paths[3], paths[4], paths[5],
                    BG_ADVENTURE
                )
                filename = f"battle_{attacker_id}.png"
                battle_file = discord.File(buffer, filename=filename)

                for c in battle_attacker_team:
                    c.team      = battle_attacker_team
                    c.enemyTeam = battle_defender_team

                # --- Gán team/enemyTeam cho defender ---
                for c in battle_defender_team:
                    c.team      = battle_defender_team
                    c.enemyTeam = battle_attacker_team

                # 1) Gửi embed log ban đầu kèm ảnh
                initial_desc = []
                initial_desc.append("**Team Tấn Công**")
                for c in battle_attacker_team:
                    initial_desc.append(
                        f"{c.name}"
                        f"⚔️{c.base_damage}  🛡️{c.armor}  💥{c.crit_rate:.0%}  🏃{c.speed:.0%}  🔋{c.chakra}"
                    )
                    initial_desc.append(f"{c.health_bar()}\n")
                initial_desc.append("\n**Team Phòng Thủ**")
                for c in battle_defender_team:
                    initial_desc.append(
                        f"{c.name}"
                        f"⚔️{c.base_damage}  🛡️{c.armor}  💥{c.crit_rate:.0%}  🏃{c.speed:.0%}  🔋{c.chakra}"
                    )
                    initial_desc.append(f"{c.health_bar()}\n")
                initial_desc.append("\nĐang khởi đầu trận đấu…")

                filename = f"battle_{attacker_id}.png"
                battle_file = discord.File(buffer, filename=filename)

                log_embed = discord.Embed(
                    title=f"🔎 {attacker.username} đi khám phá và bị {teamName} phục kích",
                    description="\n".join(initial_desc),
                    color=discord.Color.blurple()
                )
                log_embed.set_image(url=f"attachment://{filename}")

                # Gửi embed log đầu tiên, giữ lại message để edit
                log_msg = await interaction.followup.send(
                    embed=log_embed,
                    file=battle_file,
                    wait=True
                )

                # xác định thứ tự lượt: first_team đánh trước, rồi second_team
                first_team, second_team = (
                    (battle_attacker_team, battle_defender_team)
                    if get_team_total_speed(battle_attacker_team) >= get_team_total_speed(battle_defender_team)
                    else
                    (battle_defender_team, battle_attacker_team)
                )

                MAX_ROUNDS = 120
                turn = 1
                # --- bắt đầu vòng fight (mỗi turn cả 2 đội đánh) ---
                while is_team_alive(battle_attacker_team) and is_team_alive(battle_defender_team) and turn <= MAX_ROUNDS:
                # vòng 2 pha: first_team đánh, rồi nếu bên kia vẫn còn sống thì second_team đánh
                    for atk_team, def_team in ((first_team, second_team), (second_team, first_team)):
                        for c in atk_team:
                            if not c.is_alive():
                                continue

                            # 1) chỉ chạy 1 lượt của c
                            logs = battle_turn([c], def_team)

                            # 2) build lại block thông tin 6 thẻ
                            static_lines = ["**Team Tấn Công**"]
                            for x in battle_attacker_team:
                                static_lines.append(
                                    f"{x.name}"
                                    f"⚔️{x.base_damage}  🛡️{x.armor}  💥{x.crit_rate:.0%}  🏃{x.speed:.0%}  🔋{x.chakra}"
                                )
                                static_lines.append(x.health_bar() + "\n")
                            static_lines.append("\n**Team Phòng Thủ**")
                            for x in battle_defender_team:
                                static_lines.append(
                                    f"{x.name}"
                                    f"⚔️{x.base_damage}  🛡️{x.armor}  💥{x.crit_rate:.0%}  🏃{x.speed:.0%}  🔋{x.chakra}"
                                )
                                static_lines.append(x.health_bar() + "\n")

                            # 3) build rồi edit embed
                            desc = "\n".join(static_lines)
                            desc += f"\n--- Lượt {turn}: {c.name} ---\n"
                            desc += "\n".join(logs)

                            edit_embed = discord.Embed(
                                title=f"🔎 {attacker.username} đi khám phá và bị {teamName} phục kích",
                                description=desc,
                                color=discord.Color.blurple()
                            )
                            edit_embed.set_image(url=f"attachment://{filename}")

                            await log_msg.edit(embed=edit_embed)
                            await asyncio.sleep(2)
                            turn += 1

                            # nếu đã phế hết def_team, thoát sớm
                            if not is_team_alive(def_team):
                                break
                        if not is_team_alive(def_team):
                            break
                    # kiểm tra lại để thoát vòng tổng
                    if not (is_team_alive(battle_attacker_team) and is_team_alive(battle_defender_team)):
                        break

                bonus_reward = 0  # số tiền thưởng dựa trên việc đánh bại đối thủ
                session.refresh(attacker)
                # xác định người thắng
                if turn > MAX_ROUNDS:
                    result = "🏳️ Hoà"
                    outcome_text = "⚔️ Hai đội đều rút lui nên hoà! không nhận được thưởng, hãy quay lại sau 5 phút."
                    thuong = f"💰**Thưởng:** {bonus_reward:,} Ryo"
                elif is_team_alive(battle_attacker_team):
                    result = "Chiến Thắng"
                    bonus_reward = random.randint(30000, 50000)
                    attacker.coin_balance += bonus_reward
                    outcome_text = f"bạn đã chiến thắng {teamName} và đã nhận thưởng, hãy quay lại sau 5 phút."
                    thuong = f"💰**Thưởng:** nhặt được {bonus_reward:,} Ryo từ xác của {teamName}"
                else:
                    result = "Thất Bại"
                    outcome_text = f"bạn đã thất bại trước {teamName} và không nhận được gì, hãy quay lại sau 5 phút."
                    thuong = f"💰**Thưởng:** bọn {teamName} nói bạn quá non và không thèm lấy tiền của bạn"

                session.commit()

                # 3) Gửi embed kết quả cuối cùng
                result_embed = discord.Embed(
                    title=f"🏁 Kết quả trận chiến của {attacker.username} VS {teamName}",
                    description=(
                        f"🎖️ **Kết quả:** {result}\n"
                        f"{thuong}\n\n"
                        f"{outcome_text}"
                    ),
                    color=discord.Color.green() if bonus_reward != 0 else discord.Color.red()
                )
                result_embed.set_footer(text=f"Điểm Rank: {attacker.rank_points}")
                await interaction.followup.send(embed=result_embed)

        except Exception as e:
            tb = traceback.format_exc()
            await interaction.followup.send(
                f"❌ Có lỗi xảy ra:\n```{tb}```",
                ephemeral=True
            )
    @adventure.error
    async def buycard_error(self, interaction: discord.Interaction, error):
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                f"⏱️ Bạn phải chờ **{error.retry_after:.1f}** giây nữa mới đi khám phá được.",
                ephemeral=True
            )
        else:
            # Với lỗi khác, ta vẫn raise lên để discord.py xử hoặc log
            raise error
async def setup(bot):
    await bot.add_cog(Adventure(bot))