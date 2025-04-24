import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
import traceback

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.config.imageMap import CARD_IMAGE_LOCAL_PATH_MAP, BG_FIGHT, NON_CARD_PATH
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


class Fight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_fights: set[int] = set()

    @app_commands.command(name="fight", description="Thách đấu người chơi cùng trình độ")
    async def fight(self, interaction: discord.Interaction):
        attacker_id = interaction.user.id
        if attacker_id in self.active_fights:
            await interaction.response.send_message(
            "⚠️ Bạn đang trong trận đấu, vui lòng chờ cho trận trước kết thúc rồi mới /fight tiếp!",
            ephemeral=True
            )
            return
        
        await interaction.response.defer(thinking=True)
        try:
            with getDbSession() as session:
                # Lấy các repository cần thiết
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                
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
                
                # Tìm các đối thủ có rank_points trong khoảng [attacker.rank_points - 50, attacker.rank_points + 50] (ngoại trừ attacker)
                minRank = attacker.rank_points - 50
                maxRank = attacker.rank_points + 50
                opponents = session.query(Player).filter(
                    Player.player_id != attacker_id,
                    Player.rank_points >= minRank,
                    Player.rank_points <= maxRank
                ).all()
                
                # Lọc lại chỉ những người đã lắp thẻ
                valid_opponents = []
                for opp in opponents:
                    oppSetup = activeSetupRepo.getByPlayerId(opp.player_id)
                    # chỉ lấy những ai đã lắp đủ 3 thẻ (card_slot1/2/3 đều khác None)
                    if (
                        oppSetup
                        and oppSetup.card_slot1 is not None
                        and oppSetup.card_slot2 is not None
                        and oppSetup.card_slot3 is not None
                    ):
                        valid_opponents.append(opp)

                if not valid_opponents:
                    await interaction.followup.send("⚠️ Chưa tìm thấy đối thủ cùng trình độ.")
                    return

                defender = random.choice(valid_opponents)

                defenderSetup = activeSetupRepo.getByPlayerId(defender.player_id)
                # Lấy ra list 3 PlayerCard của defender
                defender_slots = [
                    defenderSetup.card_slot1,
                    defenderSetup.card_slot2,
                    defenderSetup.card_slot3,
                ]
                defender_cards = [cardRepo.getById(cid) for cid in defender_slots]

                # lấy vũ khí 
                defender_weapon_slots = [
                    defenderSetup.weapon_slot1,
                    defenderSetup.weapon_slot2,
                    defenderSetup.weapon_slot3,
                ]
                defender_weapons = [
                    weaponRepo.getById(wsid) if wsid is not None else None
                    for wsid in defender_weapon_slots
                ]

                battle_defender_team = []
                for pc, pw in zip(defender_cards, defender_weapons):
                    params = get_battle_card_params(pc, pw)
                    battle_defender_team.append(create_card(*params))

                paths = []
                for pc in attacker_cards + defender_cards:
                    key = pc.template.image_url
                    # nếu không tìm thấy key trong map thì fallback sang NON_CARD_PATH nếu bạn có
                    img_path = CARD_IMAGE_LOCAL_PATH_MAP.get(key, NON_CARD_PATH)
                    paths.append(img_path)

                # paths bây giờ là [a1, a2, a3, d1, d2, d3]

                # 2) Gọi renderImageFight
                buffer = renderImageFight(
                    paths[0], paths[1], paths[2],
                    paths[3], paths[4], paths[5],
                    BG_FIGHT
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

                self.active_fights.add(attacker_id)

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
                    title=f"🔥 Battle Log {attacker.username} VS {defender.username}",
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
                                title=f"🔥 Battle Log {attacker.username} VS {defender.username}",
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
                bonus_highest = 0 # thưởng khi đạt được thành tích cao mới
            with getDbSession() as session2:
                playerRepo2 = PlayerRepository(session2)
                fresh_attacker = playerRepo2.getById(attacker_id) 
                # xác định người thắng
                if turn > MAX_ROUNDS:
                    result = "🏳️ Hoà"
                    fresh_attacker.winning_streak = 0
                    outcome_text = "⚔️ Hai đội quá cân sức (120 vòng) nên hoà! không bên nào được thưởng."
                elif is_team_alive(battle_attacker_team):
                    dailyTaskRepo.updateFightWin(fresh_attacker.player_id)
                    fresh_attacker.rank_points += 10
                    defender.rank_points = max(0, defender.rank_points - 5)
                    defender.winning_streak = 0
                    fresh_attacker.winning_streak += 1
                    bonus_reward = 500 * fresh_attacker.winning_streak
                    if fresh_attacker.rank_points > fresh_attacker.highest_rank_points:
                        bonus_highest = 5000
                        fresh_attacker.highest_rank_points = fresh_attacker.rank_points
                    fresh_attacker.coin_balance += bonus_reward + bonus_highest
                    result = "Chiến Thắng"
                    outcome_text = f"**Điểm Rank:**{fresh_attacker.username} +10 điểm, {defender.username} -5 điểm"
                else:
                    fresh_attacker.rank_points = max(0, fresh_attacker.rank_points - 10)
                    defender.rank_points += 5
                    fresh_attacker.winning_streak = 0
                    result = "Thất Bại"
                    outcome_text = f" **Điểm Rank:** {fresh_attacker.username} -10 điểm, {defender.username} +5 điểm"

                session2.commit()

                # 3) Gửi embed kết quả cuối cùng
                result_embed = discord.Embed(
                    title=f"🏁 Kết quả trận chiến của {fresh_attacker.username} VS {defender.username}",
                    description=(
                        f"🎖️ **Kết quả:** {result}\n"
                        f"💰**Thưởng:** {bonus_reward + bonus_highest:,} Ryo\n"
                        f"🏆**Chuỗi thắng:** {fresh_attacker.winning_streak}\n"
                        f"{outcome_text}"
                    ),
                    color=discord.Color.green() if bonus_reward != 0 else discord.Color.red()
                )
                result_embed.set_footer(text=f"Điểm Rank: {fresh_attacker.rank_points}")
                await interaction.followup.send(embed=result_embed)

        except Exception as e:
            tb = traceback.format_exc()
            await interaction.followup.send(
                f"❌ Có lỗi xảy ra:\n```{tb}```",
                ephemeral=True
            )
        finally:
            self.active_fights.remove(attacker_id)

async def setup(bot):
    await bot.add_cog(Fight(bot))
