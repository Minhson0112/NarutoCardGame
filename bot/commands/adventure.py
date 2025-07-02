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
from bot.services.battle import Battle
from bot.services.help import get_battle_card_params, render_team_status, get_adventure_effective_stats
from bot.services.createCard import create_card

class Adventure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name= "adventure", description= "đi thám hiểm, dẹp loạn, nhận ryo nếu thắng")
    @app_commands.describe(
        difficulty="độ khó"
    )
    @app_commands.choices(difficulty=[
        app_commands.Choice(name="Dễ", value="easy"),
        app_commands.Choice(name="Trung Bình", value="medium"),
        app_commands.Choice(name="Khó", value="hard")
    ])
    @checks.cooldown(1, 300, key=lambda interaction: interaction.user.id)
    async def adventure(self, interaction: discord.Interaction,  difficulty: str):
        attacker_id = interaction.user.id
        await interaction.response.defer(thinking=True)
        
        teamNames = ["Team thích thể hiện", "Team phổi to", "Team phá làng phá xóm", "Team giang hồ mõm",
                    "Team cung bọ cạp", "Team biết bố mày là ai không", "Team chọc gậy bánh xe", "Team nghiện cờ bạc",
                    "Team con nhà người ta", "Team thì ra mày chọn cái chết", "Team mình tao chấp hết",
                    "Team tao có kiên", "Team hacker lỏ", "Team Không trượt phát lào", "Team tuổi l sánh vai", "Team đầu chộm đuôi cướp",
                    "Team buôn hàng nóng", "Team gấu tró", "Team máu dồn lên não", "Team wibu", "Team fan mu", "Team đáy xã hội",
                    "Team phụ hồ", "Team Ca sĩ hàn quốc", "Team đom đóm", "Team hội mê peter"]
        teamName = random.choice(teamNames)

        weaponName = ["Kunai", "Knife", "ChakraKnife", "Guandao", "Katana", "Shuriken", "Bow", "Flail", "Kibaku", "Tansa", "Tessen", "Sansaju", "Suna", "Enma", "Samehada", "Rinnegan", "Gudodama"]
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

                defenderCardLevel = 1
                weapon_name = None
                battle_defender_team = []
                defenderCardImgPaths = []
                list_card = cardtemplaterepo.getFormationTemplates()
                for card in list_card:
                    if (difficulty == "easy"):
                        defenderCardLevel = 1
                    elif (difficulty == "medium"):
                        defenderCardLevel = random.randint(10, 20)
                        weapon_name = random.choice(weaponName)
                    elif (difficulty == "hard"):
                        defenderCardLevel = random.randint(30, 50)
                        weapon_name = random.choice(weaponName)
                        
                    img_path = CARD_IMAGE_LOCAL_PATH_MAP.get(card.image_url, NON_CARD_PATH)
                    params = get_adventure_effective_stats(card.name, card.health, card.armor, card.base_damage, card.crit_rate, card.speed, card.chakra, card.element, card.tier, defenderCardLevel, weapon_name)
                    battle_card = create_card(*params)
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
                initial_desc += render_team_status(battle_attacker_team, "**Team Tấn Công**")
                initial_desc += render_team_status(battle_defender_team, "**Team Phòng Thủ**")
                initial_desc.append("\nĐang khởi đầu trận đấu…")

                log_embed = discord.Embed(
                    title=f"🔎 {attacker.username} đi khám phá và bị {teamName} phục kích",
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
                                title=f"🔎 {attacker.username} đi khám phá và bị {teamName} phục kích",
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
            with getDbSession() as session2:
                playerRepo2 = PlayerRepository(session2)
                fresh_attacker = playerRepo2.getById(attacker_id) 
                # xác định người thắng
                if battle.turn >= battle.maxturn:
                    result = "🏳️ Hoà"
                    outcome_text = "⚔️ Hai đội đều rút lui nên hoà! không nhận được thưởng, hãy quay lại sau 5 phút."
                    thuong = f"💰**Thưởng:** {bonus_reward:,} Ryo"
                elif battle.is_team_alive(battle.attacker_team):
                    result = "Chiến Thắng"
                    bonus_reward = random.randint(30000, 50000)
                    fresh_attacker.coin_balance += bonus_reward
                    outcome_text = f"bạn đã chiến thắng {teamName} và đã nhận thưởng, hãy quay lại sau 5 phút."
                    thuong = f"💰**Thưởng:** nhặt được {bonus_reward:,} Ryo từ xác của {teamName}"
                else:
                    result = "Thất Bại"
                    outcome_text = f"bạn đã thất bại trước {teamName} và không nhận được gì, hãy quay lại sau 5 phút."
                    thuong = f"💰**Thưởng:** bọn {teamName} nói bạn quá non và không thèm lấy tiền của bạn"
                
                fresh_attacker.exp += 10
                session2.commit()
                # 3) Gửi embed kết quả cuối cùng
                result_embed = discord.Embed(
                    title=f"🏁 Kết quả trận chiến của {fresh_attacker.username} VS {teamName}",
                    description=(
                        f"🎖️ **Kết quả:** {result}\n"
                        f"{thuong}\n\n"
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