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
from bot.services.battle import Battle
from bot.services.help import get_battle_card_params, render_team_status
from bot.services.createCard import create_card

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
                # Lấy danh sách Top10 (theo rank_points desc)
                # top10 = playerRepo.getTop10()
                # top10_ids = [p.player_id for p in top10]

                # if attacker_id in top10_ids:
                #     # attacker nằm trong Top10 → dùng index để tìm đối thủ
                #     idx = top10_ids.index(attacker_id)
                #     if idx == 0:
                #         # đứng đầu Top10
                #         await interaction.followup.send("⚠️ Bạn đang ở Top 1, không có đối thủ.")
                #         return
                #     # đối thủ là người đứng ngay trước trong list
                #     defender = top10[idx - 1]

                #     # kiểm tra đã lắp đội hình chưa
                #     oppSetup = activeSetupRepo.getByPlayerId(defender.player_id)
                #     if not (oppSetup and oppSetup.card_slot1 and oppSetup.card_slot2 and oppSetup.card_slot3):
                #         await interaction.followup.send("⚠️ Người chơi xếp trên chưa lắp đủ đội hình.")
                #         return

                # else:
                #     # attacker không nằm trong Top10 → fallback về logic ±20
                #     minRank = attacker.rank_points - 30
                #     maxRank = attacker.rank_points + 30
                #     opponents = session.query(Player).filter(
                #         Player.player_id != attacker_id,
                #         Player.rank_points.between(minRank, maxRank)
                #     ).all()

                #     valid_opponents = []
                #     for opp in opponents:
                #         oppSetup = activeSetupRepo.getByPlayerId(opp.player_id)
                #         if oppSetup and oppSetup.card_slot1 and oppSetup.card_slot2 and oppSetup.card_slot3:
                #             valid_opponents.append(opp)

                #     if not valid_opponents:
                #         await interaction.followup.send("⚠️ Chưa tìm thấy đối thủ cùng trình độ.")
                #         return

                #     defender = random.choice(valid_opponents)

                minRank = attacker.rank_points - 30
                maxRank = attacker.rank_points + 30
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
                    top10 = playerRepo.getTop10()
                    top10_ids = [p.player_id for p in top10]
                    
                    if attacker_id in top10_ids:
                        # attacker nằm trong Top10 → dùng index để tìm đối thủ
                        idx = top10_ids.index(attacker_id)
                        if idx == 0:
                            # đứng đầu Top10
                            await interaction.followup.send("⚠️ Bạn đang ở Top 1, không có đối thủ.")
                            return
                        # đối thủ là người đứng ngay trước trong list
                        defender = top10[idx - 1]
                else:
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
                initial_desc += render_team_status(battle_attacker_team, "**Team Tấn Công**")
                initial_desc += render_team_status(battle_defender_team, "**Team Phòng Thủ**")
                initial_desc.append("\nĐang khởi đầu trận đấu…")

                log_embed = discord.Embed(
                    title=f"🔥 Battle Log {attacker.username} VS {defender.username}",
                    description="\n".join(initial_desc),
                    color=discord.Color.blurple()
                )
                log_embed.set_image(url=f"attachment://{filename}")
                log_msg = await interaction.followup.send(
                    embed=log_embed,
                    file=battle_file,
                    wait=True
                )

                #..........................battle.................................
                battle = Battle(battle_attacker_team, battle_defender_team, maxturn=120)
                while (
                    battle.is_team_alive(battle.attacker_team) and
                    battle.is_team_alive(battle.defender_team) and
                    battle.turn <= battle.maxturn
                ):
                    for atk_team, def_team in (
                        (battle.first_team, battle.second_team),
                        (battle.second_team, battle.first_team)
                    ):
                        for c in atk_team:
                            if not c.is_alive():
                                continue
                            logs = battle.battle_turn_one_card(c)
                            static_lines = []
                            static_lines += render_team_status(battle_attacker_team, "**Team Tấn Công**")
                            static_lines += render_team_status(battle_defender_team, "**Team Phòng Thủ**")
                            desc = "\n".join(static_lines)
                            desc += f"\n--- Lượt {battle.turn}: {c.name} ---\n"
                            desc += "\n".join(logs)

                            edit_embed = discord.Embed(
                                title=f"🔥 Battle Log {attacker.username} VS {defender.username}",
                                description=desc,
                                color=discord.Color.blurple()
                            )
                            edit_embed.set_image(url=f"attachment://{filename}")
                            await log_msg.edit(embed=edit_embed)
                            await asyncio.sleep(2)
                            battle.turn += 1
                            if not battle.is_team_alive(def_team):
                                break
                        if not battle.is_team_alive(def_team):
                            break

                bonus_reward = 0  # số tiền thưởng dựa trên việc đánh bại đối thủ
                bonus_highest = 0 # thưởng khi đạt được thành tích cao mới
            with getDbSession() as session2:
                playerRepo2 = PlayerRepository(session2)
                fresh_attacker = playerRepo2.getById(attacker_id) 
                fresh_defender = playerRepo2.getById(defender.player_id) 
                # xác định người thắng
                if battle.turn >= battle.maxturn:
                    result = "🏳️ Hoà"
                    fresh_attacker.winning_streak = 0
                    outcome_text = "⚔️ Hai đội quá cân sức (120 vòng) nên hoà! không bên nào được thưởng."
                elif battle.is_team_alive(battle.attacker_team):
                    dailyTaskRepo.updateFightWin(fresh_attacker.player_id)
                    fresh_attacker.rank_points += 10
                    fresh_defender.rank_points = max(0, fresh_defender.rank_points - 5)
                    fresh_defender.winning_streak = 0
                    fresh_attacker.winning_streak += 1
                    bonus_reward = 500 * fresh_attacker.winning_streak
                    if fresh_attacker.rank_points > fresh_attacker.highest_rank_points:
                        bonus_highest = 5000
                        fresh_attacker.highest_rank_points = fresh_attacker.rank_points
                    fresh_attacker.coin_balance += bonus_reward + bonus_highest
                    result = "Chiến Thắng"
                    outcome_text = f"**Điểm Rank:**{fresh_attacker.username} +10 điểm, {fresh_defender.username} -5 điểm"
                else:
                    fresh_attacker.rank_points = max(0, fresh_attacker.rank_points - 10)
                    fresh_defender.rank_points += 5
                    fresh_attacker.winning_streak = 0
                    result = "Thất Bại"
                    outcome_text = f" **Điểm Rank:** {fresh_attacker.username} -10 điểm, {fresh_defender.username} +5 điểm"

                session2.commit()

                # 3) Gửi embed kết quả cuối cùng
                result_embed = discord.Embed(
                    title=f"🏁 Kết quả trận chiến của {fresh_attacker.username} VS {fresh_defender.username}",
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
