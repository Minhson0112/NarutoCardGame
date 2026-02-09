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
from bot.repository.weaponTemplateRepository import WeaponTemplateRepository

from bot.config.imageMap import CARD_IMAGE_LOCAL_PATH_MAP, TAILED_IMAGE_LOCAL_PATH_MAP, BG_TAILED, NON_CARD_PATH
from bot.config.gachaConfig import GACHA_DROP_RATE
from bot.config.weaponGachaConfig import WEAPON_GACHA_DROP_RATE
from bot.services.tailedRender import renderImageFight
from bot.services.battle import Battle
from bot.services.help import get_battle_card_params, render_team_status, get_tailed_effective_stats
from bot.services.createCard import create_card
from bot.services.i18n import t


class TailedBoss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="tailedboss", description="săn vĩ thú nhận ryo, thẻ và vũ khí")
    @app_commands.describe(difficulty="độ khó")
    @app_commands.choices(difficulty=[
        app_commands.Choice(name="Dễ", value="easy"),
        app_commands.Choice(name="Trung Bình", value="medium"),
        app_commands.Choice(name="Khó", value="hard")
    ])
    @checks.cooldown(1, 3600, key=lambda interaction: interaction.user.id)
    async def tailedboss(self, interaction: discord.Interaction, difficulty: str):
        attacker_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        await interaction.response.defer(thinking=True)

        type1OfTailed = ["1vi", "2vi", "3vi", "4vi", "5vi", "6vi", "7vi"]

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                cardtemplaterepo = CardTemplateRepository(session)
                playerCardRepo = PlayerCardRepository(session)
                weaponTemplateRepo = WeaponTemplateRepository(session)
                playerWeaponRepo = PlayerWeaponRepository(session)

                attacker = playerRepo.getById(attacker_id)
                if not attacker:
                    await interaction.followup.send(t(guild_id, "tailedboss.not_registered"))
                    return

                attackerSetup = activeSetupRepo.getByPlayerId(attacker_id)

                slots = [
                    attackerSetup.card_slot1,
                    attackerSetup.card_slot2,
                    attackerSetup.card_slot3,
                ]
                if any(slot is None for slot in slots):
                    await interaction.followup.send(t(guild_id, "tailedboss.need_full_team"))
                    return

                attacker_cards = [cardRepo.getById(slot_id) for slot_id in slots]

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
                    params = get_battle_card_params(pc, pw)
                    battle_card = create_card(*params, guild_id=guild_id)
                    battle_attacker_team.append(battle_card)

                tailedCardlevel = 1
                if difficulty == "easy":
                    tailedCardlevel = 1
                elif difficulty == "medium":
                    tailedCardlevel = random.randint(2, 6)
                elif difficulty == "hard":
                    tailedCardlevel = random.randint(7, 10)

                battle_defender_team = []
                defenderCardImgPaths = []
                list_cards = cardtemplaterepo.getRandomTailedCard()

                for card in list_cards:
                    img_path = TAILED_IMAGE_LOCAL_PATH_MAP.get(card.image_url, NON_CARD_PATH)
                    taileCard = get_tailed_effective_stats(
                        card.name,
                        card.health,
                        card.armor,
                        card.base_damage,
                        card.crit_rate,
                        card.speed,
                        card.chakra,
                        card.element,
                        card.tier,
                        tailedCardlevel,
                        weapon_name=None
                    )
                    battle_card = create_card(*taileCard, guild_id=guild_id)
                    battle_defender_team.append(battle_card)
                    defenderCardImgPaths.append(img_path)

                attackCardImgpaths = []
                for pc in attacker_cards:
                    key = pc.template.image_url
                    img_path = CARD_IMAGE_LOCAL_PATH_MAP.get(key, NON_CARD_PATH)
                    attackCardImgpaths.append(img_path)

                paths = attackCardImgpaths + defenderCardImgPaths
                buffer = renderImageFight(paths[0], paths[1], paths[2], paths[3], BG_TAILED)
                filename = f"battle_{attacker_id}.png"
                battle_file = discord.File(buffer, filename=filename)

                for c in battle_attacker_team:
                    c.team = battle_attacker_team
                    c.enemyTeam = battle_defender_team

                for c in battle_defender_team:
                    c.team = battle_defender_team
                    c.enemyTeam = battle_attacker_team

                boss_name = list_cards[0].name

                initial_desc = []
                initial_desc += render_team_status(battle_attacker_team, t(guild_id, "tailedboss.team.attacker"))
                initial_desc += render_team_status(battle_defender_team, t(guild_id, "tailedboss.team.defender"))
                initial_desc.append("\n" + t(guild_id, "tailedboss.battle.starting"))

                log_embed = discord.Embed(
                    title=t(
                        guild_id,
                        "tailedboss.log.title",
                        username=attacker.username,
                        boss=boss_name,
                        level=tailedCardlevel
                    ),
                    description="\n".join(initial_desc),
                    color=discord.Color.blurple()
                )
                log_embed.set_image(url=f"attachment://{filename}")
                log_msg = await interaction.followup.send(
                    embed=log_embed,
                    file=battle_file,
                    wait=True
                )

                battle = Battle(battle_attacker_team, battle_defender_team, maxturn=200, guild_id=guild_id)

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
                            static_lines += render_team_status(battle_attacker_team, t(guild_id, "tailedboss.team.attacker"))
                            static_lines += render_team_status(battle_defender_team, t(guild_id, "tailedboss.team.defender"))

                            desc = "\n".join(static_lines)
                            desc += "\n" + t(guild_id, "tailedboss.battle.turn_header", turn=battle.turn, name=c.name) + "\n"
                            desc += "\n".join(logs)

                            edit_embed = discord.Embed(
                                title=t(
                                    guild_id,
                                    "tailedboss.log.title",
                                    username=attacker.username,
                                    boss=boss_name,
                                    level=tailedCardlevel
                                ),
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

            bonus_reward = 0
            damageDead = 0

            with getDbSession() as session2:
                playerRepo2 = PlayerRepository(session2)
                fresh_attacker = playerRepo2.getById(attacker_id)

                if battle.turn >= battle.maxturn:
                    result_key = "tailedboss.result.draw"
                    outcome_text = t(guild_id, "tailedboss.result.draw_text", boss=boss_name)

                    damageDead = battle_defender_team[0].max_health - battle_defender_team[0].health
                    bonus_reward = damageDead * 50
                    fresh_attacker.coin_balance += bonus_reward

                    damageDeadTxt = t(guild_id, "tailedboss.result.damage_text", damage=damageDead, boss=boss_name)
                    thuong = t(guild_id, "tailedboss.result.reward_money_only", money=bonus_reward)

                elif battle.is_team_alive(battle.attacker_team):
                    result_key = "tailedboss.result.win"
                    outcome_text = t(guild_id, "tailedboss.result.win_text", boss=boss_name)

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

                        thuong = t(
                            guild_id,
                            "tailedboss.result.reward_money_card",
                            boss=boss_name,
                            money=bonus_reward,
                            card=card.name,
                            tier=card.tier
                        )
                    else:
                        rates = WEAPON_GACHA_DROP_RATE["weapon_pack"]
                        tiers = list(rates.keys())
                        weights = list(rates.values())
                        outcomeTier = random.choices(tiers, weights=weights, k=1)[0]
                        weapon = weaponTemplateRepo.getRandomByGrade(outcomeTier)
                        playerWeaponRepo.incrementQuantity(attacker_id, weapon.weapon_key, increment=1)

                        thuong = t(
                            guild_id,
                            "tailedboss.result.reward_money_weapon",
                            boss=boss_name,
                            money=bonus_reward,
                            weapon=weapon.name,
                            grade=weapon.grade
                        )

                    damageDeadTxt = t(guild_id, "tailedboss.result.damage_text", damage=damageDead, boss=boss_name)

                else:
                    result_key = "tailedboss.result.lose"
                    outcome_text = t(guild_id, "tailedboss.result.lose_text", boss=boss_name)

                    damageDead = battle_defender_team[0].max_health - battle_defender_team[0].health
                    bonus_reward = damageDead * 25
                    fresh_attacker.coin_balance += bonus_reward

                    damageDeadTxt = t(guild_id, "tailedboss.result.damage_text", damage=damageDead, boss=boss_name)
                    thuong = t(guild_id, "tailedboss.result.reward_money_only", money=bonus_reward)

                fresh_attacker.exp += 10
                session2.commit()

                result_value = t(guild_id, result_key)
                result_embed = discord.Embed(
                    title=t(guild_id, "tailedboss.result.embed_title", player=fresh_attacker.username, boss=boss_name),
                    description=(
                        t(guild_id, "tailedboss.result.embed_result", result=result_value)
                        + "\n"
                        + f"{thuong}\n\n"
                        + f"{damageDeadTxt}\n\n"
                        + f"{outcome_text}"
                    ),
                    color=discord.Color.green() if result_key == "tailedboss.result.win" else discord.Color.red()
                )
                result_embed.set_footer(text=f"Điểm Rank: {fresh_attacker.rank_points}")
                await interaction.followup.send(embed=result_embed)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(
                f"{t(guild_id, 'tailedboss.error')}\n```{tb}```",
                ephemeral=True
            )

    @tailedboss.error
    async def tailedboss_error(self, interaction: discord.Interaction, error):
        guild_id = interaction.guild.id if interaction.guild else None

        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                t(guild_id, "tailedboss.cooldown", seconds=error.retry_after),
                ephemeral=True
            )
            return

        raise error


async def setup(bot):
    await bot.add_cog(TailedBoss(bot))
