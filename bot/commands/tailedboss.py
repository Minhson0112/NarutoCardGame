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
from bot.config.imageMap import CARD_IMAGE_LOCAL_PATH_MAP,TAILED_IMAGE_LOCAL_PATH_MAP , BG_ADVENTURE, NON_CARD_PATH
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

class TailedBoss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name= "tailedboss", description= "săn vĩ thú nhận ryo, thẻ và vũ khí")
    @checks.cooldown(1, 300, key=lambda interaction: interaction.user.id)
    async def tailedboss(self, interaction: discord.Interaction):
        attacker_id = interaction.user.id
        await interaction.response.defer(thinking=True)

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
                list_cards = cardtemplaterepo.getRandomTailedCard()
                for card in list_cards:
                    img_path = TAILED_IMAGE_LOCAL_PATH_MAP.get(card.image_url, NON_CARD_PATH)
                    battle_card = create_card(card.name, card.health, card.armor, card.base_damage, card.crit_rate, card.speed, card.chakra, card.element, card.tier)
                    battle_defender_team.append(battle_card)
                    defenderCardImgPaths.append(img_path)
                
                