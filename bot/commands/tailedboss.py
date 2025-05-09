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
from bot.repository.playerCardRepository import PlayerCardRepository
from bot.repository.weaponTemplateRepository import WeaponTemplateRepository
from bot.repository.playerWeaponRepository import PlayerWeaponRepository
from bot.config.imageMap import CARD_IMAGE_LOCAL_PATH_MAP,TAILED_IMAGE_LOCAL_PATH_MAP , BG_TAILED, NON_CARD_PATH
from bot.config.gachaConfig import GACHA_DROP_RATE
from bot.config.weaponGachaConfig import WEAPON_GACHA_DROP_RATE
from bot.services.tailedRender import renderImageFight
from bot.services.battle import Battle
from bot.services.help import get_battle_card_params, render_team_status
from bot.services.createCard import create_card

class TailedBoss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name= "tailedboss", description= "săn vĩ thú nhận ryo, thẻ và vũ khí")
    @checks.cooldown(1, 3600, key=lambda interaction: interaction.user.id)
    async def tailedboss(self, interaction: discord.Interaction):
        attacker_id = interaction.user.id
        await interaction.response.defer(thinking=True)

        type1OfTailed = ["1vi", "2vi", "3vi", "4vi", "5vi", "6vi", "7vi"]

        try:
            with getDbSession() as session:
                # Lấy các repository cần thiết
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                cardtemplaterepo = CardTemplateRepository(session)
                playerCardRepo = PlayerCardRepository(session)
                weaponTemplateRepo = WeaponTemplateRepository(session)
                playerWeaponRepo = PlayerWeaponRepository(session)

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
                list_cards = cardtemplaterepo.getRandomTailedCard()
                for card in list_cards:
                    img_path = TAILED_IMAGE_LOCAL_PATH_MAP.get(card.image_url, NON_CARD_PATH)
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
                    paths[0], paths[1], paths[2],paths[3],BG_TAILED
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
                    title=f"🦊 {attacker.username} đã tìm thấy {list_cards[0].name} trong hang",
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
                battle = Battle(battle_attacker_team, battle_defender_team, maxturn=200)
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
                                title=f"🦊 {attacker.username} đã tìm thấy {list_cards[0].name} trong hang",
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
                damageDead = 0 # sát thương gây ra lên boss
            with getDbSession() as session2:
                playerRepo2 = PlayerRepository(session2)
                fresh_attacker = playerRepo2.getById(attacker_id) 
                # xác định người thắng
                if battle.turn >= battle.maxturn:
                    result = "🏳️ Hoà"
                    outcome_text = f"⚔️ sau 200 lượt bạn không hạ được {list_cards[0].name} nên hòa, hãy quay lại sau 1 tiếng"
                    damageDead = battle_defender_team[0].max_health - battle_defender_team[0].health
                    bonus_reward = damageDead * 50
                    fresh_attacker.coin_balance += bonus_reward
                    damageDeadTxt = f"bạn đã gây ra {damageDead} sát thương lên {list_cards[0].name}"
                    thuong = f"💰**Thưởng:** {bonus_reward:,} Ryo"
                elif battle.is_team_alive(battle.attacker_team):
                    result = "Chiến Thắng"
                    damageDead = battle_defender_team[0].max_health
                    bonus_reward = damageDead * 50
                    fresh_attacker.coin_balance += bonus_reward

                    if list_cards[0].tier in type1OfTailed:
                        rates = GACHA_DROP_RATE["card_advanced"]
                        tiers = list(rates.keys())
                        weights = list(rates.values())
                        outcomeTier = random.choices(tiers, weights=weights, k=1)[0]
                        card = cardtemplaterepo.getRandomByTier(outcomeTier)
                        playerCardRepo.incrementQuantity(attacker_id, card.card_key, increment=1)
                        thuong = f"💰**Thưởng:** {list_cards[0].name} chết và rơi ra {bonus_reward:,} Ryo và thẻ {card.name}(bậc {card.tier})"
                    elif list_cards[0].tier not in type1OfTailed:
                        rates = WEAPON_GACHA_DROP_RATE["weapon_pack"]
                        tiers = list(rates.keys())
                        weights = list(rates.values())
                        outcomeTier = random.choices(tiers, weights=weights, k=1)[0]
                        weapon = weaponTemplateRepo.getRandomByGrade(outcomeTier)
                        playerWeaponRepo.incrementQuantity(attacker_id, weapon.weapon_key, increment=1)
                        thuong = f"💰**Thưởng:** {list_cards[0].name} chết và rơi ra {bonus_reward:,} Ryo và vũ khí {weapon.name}(bậc {weapon.grade})"

                    damageDeadTxt = f"bạn đã gây ra {damageDead} sát thương lên {list_cards[0].name}"
                    outcome_text = f"bạn đã chiến thắng {list_cards[0].name} và đã nhận thưởng, hãy quay lại sau 1 tiếng."
                    
                else:
                    result = "Thất Bại"
                    outcome_text = f"bạn đã bị {list_cards[0].name} đấm chết và nhận thưởng, hãy quay lại sau 1 tiếng."
                    damageDead = battle_defender_team[0].max_health - battle_defender_team[0].health
                    bonus_reward = damageDead * 50
                    fresh_attacker.coin_balance += bonus_reward
                    damageDeadTxt = f"bạn đã gây ra {damageDead} sát thương lên {list_cards[0].name}"
                    thuong = f"💰**Thưởng:** {bonus_reward:,} Ryo"

                session2.commit()

                # 3) Gửi embed kết quả cuối cùng
                result_embed = discord.Embed(
                    title=f"🏁 Kết quả trận chiến của {fresh_attacker.username} VS {list_cards[0].name}",
                    description=(
                        f"🎖️ **Kết quả:** {result}\n"
                        f"{thuong}\n\n"
                        f"{damageDeadTxt}\n\n"
                        f"{outcome_text}"
                    ),
                    color=discord.Color.green() if result == "Chiến Thắng" else discord.Color.red()
                )
                result_embed.set_footer(text=f"Điểm Rank: {fresh_attacker.rank_points}")
                await interaction.followup.send(embed=result_embed)

        except Exception as e:
            tb = traceback.format_exc()
            await interaction.followup.send(
                f"❌ Có lỗi xảy ra:\n```{tb}```",
                ephemeral=True
            )
    @tailedboss.error
    async def buycard_error(self, interaction: discord.Interaction, error):
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                f"⏱️ Bạn phải chờ **{error.retry_after:.1f}** giây nữa mới đánh được vĩ thú.",
                ephemeral=True
            )
        else:
            # Với lỗi khác, ta vẫn raise lên để discord.py xử hoặc log
            raise error

async def setup(bot):
    await bot.add_cog(TailedBoss(bot))
