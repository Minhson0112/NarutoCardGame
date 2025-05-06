import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

from bot.config.database import getDbSession
from bot.repository.playerRepository import PlayerRepository
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.repository.playerActiveSetupRepository import PlayerActiveSetupRepository
from bot.repository.dailyTaskRepository import DailyTaskRepository
from bot.config.imageMap import CARD_IMAGE_LOCAL_PATH_MAP, BG_FIGHT, NON_CARD_PATH
from bot.entity.player import Player
from bot.services.battle import Battle
from bot.services.fightRender import renderImageFight
from bot.services.help import get_battle_card_params, render_team_status
from bot.services.createCard import create_card

class FightWith(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_fights: set[int] = set()

    @app_commands.command(name="fightwith", description="Pk vui với người chơi đã tag (không cập nhật rank)")
    @app_commands.describe(
        target="Tag của người chơi bạn muốn pk"
    )
    async def fightwith(self, interaction: discord.Interaction, target: discord.Member):
        attacker_id = interaction.user.id
        defender_id = target.id
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

                if defender_id == attacker_id:
                    await interaction.followup.send("⚠️ Bạn không thể pk với chính mình.")
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

                opponents = playerRepo.getById(defender_id)
                if not opponents:
                    await interaction.followup.send("⚠️ Người chơi được tag chưa tạo tài khoản.")
                    return
                
                oppSetup = activeSetupRepo.getByPlayerId(opponents.player_id)
                if not oppSetup or any(slot is None for slot in (oppSetup.card_slot1, oppSetup.card_slot2, oppSetup.card_slot3)):
                    await interaction.followup.send("⚠️ Người chơi được tag chưa sẵn sàng pk (thiếu thẻ).")
                    return
                
                defenderSetup = oppSetup
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
                    title=f"🔥 Battle Log {attacker.username} VS {opponents.username}",
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
                                title=f"🔥 Battle Log {attacker.username} VS {opponents.username}",
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

                # xác định người thắng
                if battle.turn >= battle.maxturn:
                    result = "🏳️ Hoà"
                    outcome_text = "⚔️ Hai đội quá cân sức (120 vòng) nên hoà!."
                elif battle.is_team_alive(battle.attacker_team):
                    result = "Chiến Thắng"
                else:
                    result = "Thất Bại"

                dailyTaskRepo.updateFightwith(attacker_id)
                session.commit()
                outcome_text = f" **Điểm Rank:** vì không phải đánh rank nên không ai nhận được thưởng hay điêm rank"

                # 3) Gửi embed kết quả cuối cùng
                result_embed = discord.Embed(
                    title=f"🏁 Kết quả trận chiến của {attacker.username} VS {opponents.username}",
                    description=(
                        f"🎖️ **Kết quả:** {result}\n"
                        f"💰**Thưởng:** 0 Ryo\n"
                        f"🏆**Chuỗi thắng:** Không bị thay đổi\n"
                        f"{outcome_text}"
                    ),
                    color=discord.Color.green() if result == "Chiến Thắng" else discord.Color.red()
                )
                result_embed.set_footer(text=f"Điểm Rank: {attacker.rank_points}")
                await interaction.followup.send(embed=result_embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý fightwith:", e)
            await interaction.followup.send("❌ Có lỗi xảy ra. Vui lòng thử lại sau.")
        finally:
            self.active_fights.remove(attacker_id)
async def setup(bot):
    await bot.add_cog(FightWith(bot))
