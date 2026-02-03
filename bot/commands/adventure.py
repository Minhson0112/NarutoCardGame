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
from bot.services.fightRender import renderImageFight
from bot.services.battle import Battle
from bot.services.help import get_battle_card_params, render_team_status, get_adventure_effective_stats
from bot.services.createCard import create_card
from bot.services.i18n import t


class Adventure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="adventure", description="đi thám hiểm, dẹp loạn, nhận ryo nếu thắng")
    @app_commands.describe(difficulty="độ khó")
    @app_commands.choices(difficulty=[
        app_commands.Choice(name="Dễ", value="easy"),
        app_commands.Choice(name="Trung Bình", value="medium"),
        app_commands.Choice(name="Khó", value="hard")
    ])
    @checks.cooldown(1, 300, key=lambda interaction: interaction.user.id)
    async def adventure(self, interaction: discord.Interaction, difficulty: str):
        attacker_id = interaction.user.id
        await interaction.response.defer(thinking=True)

        guild_id = interaction.guild.id if interaction.guild else None

        team_names = t(guild_id, "adventure.team_names")
        teamName = random.choice(team_names) if isinstance(team_names, list) and team_names else "Enemy Team"

        weaponName = [
            "Kunai", "Knife", "ChakraKnife", "Guandao", "Katana", "Shuriken", "Bow", "Flail",
            "Kibaku", "Tansa", "Tessen", "Sansaju", "Suna", "Enma", "Samehada", "Rinnegan", "Gudodama"
        ]

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)
                dailyTaskRepo = DailyTaskRepository(session)
                cardtemplaterepo = CardTemplateRepository(session)

                attacker = playerRepo.getById(attacker_id)
                if not attacker:
                    await interaction.followup.send(t(guild_id, "adventure.not_registered"))
                    return

                attackerSetup = activeSetupRepo.getByPlayerId(attacker_id)

                slots = [
                    attackerSetup.card_slot1,
                    attackerSetup.card_slot2,
                    attackerSetup.card_slot3,
                ]
                if any(slot is None for slot in slots):
                    await interaction.followup.send(t(guild_id, "adventure.need_full_team"))
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
                    battle_card = create_card(*params)
                    battle_attacker_team.append(battle_card)

                defenderCardLevel = 1
                weapon_name = None
                battle_defender_team = []
                defenderCardImgPaths = []

                list_card = cardtemplaterepo.getFormationTemplates()
                for card in list_card:
                    if difficulty == "easy":
                        defenderCardLevel = 1
                    elif difficulty == "medium":
                        defenderCardLevel = random.randint(10, 20)
                        weapon_name = random.choice(weaponName)
                    elif difficulty == "hard":
                        defenderCardLevel = random.randint(30, 50)
                        weapon_name = random.choice(weaponName)

                    img_path = CARD_IMAGE_LOCAL_PATH_MAP.get(card.image_url, NON_CARD_PATH)
                    params = get_adventure_effective_stats(
                        card.name,
                        card.health,
                        card.armor,
                        card.base_damage,
                        card.crit_rate,
                        card.speed,
                        card.chakra,
                        card.element,
                        card.tier,
                        defenderCardLevel,
                        weapon_name
                    )
                    battle_card = create_card(*params)
                    battle_defender_team.append(battle_card)
                    defenderCardImgPaths.append(img_path)

                attackCardImgpaths = []
                for pc in attacker_cards:
                    key = pc.template.image_url
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
                    c.team = battle_attacker_team
                    c.enemyTeam = battle_defender_team

                for c in battle_defender_team:
                    c.team = battle_defender_team
                    c.enemyTeam = battle_attacker_team

                initial_desc = []
                initial_desc += render_team_status(battle_attacker_team, "**Attack team**")
                initial_desc += render_team_status(battle_defender_team, "**Defense team**")
                initial_desc.append("\n" + t(guild_id, "adventure.battle.starting"))

                log_embed = discord.Embed(
                    title=t(guild_id, "adventure.battle.title", username=attacker.username, teamName=teamName),
                    description="\n".join(initial_desc),
                    color=discord.Color.blurple()
                )
                log_embed.set_image(url=f"attachment://{filename}")
                log_msg = await interaction.followup.send(
                    embed=log_embed,
                    file=battle_file,
                    wait=True
                )

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
                            static_lines += render_team_status(battle_attacker_team, "**Attack team**")
                            static_lines += render_team_status(battle_defender_team, "**Defense team**")

                            desc = "\n".join(static_lines)
                            desc += "\n" + t(
                                guild_id,
                                "adventure.battle.turn_header",
                                turn=battle.turn,
                                cardName=c.name
                            ) + "\n"
                            desc += "\n".join(logs)

                            edit_embed = discord.Embed(
                                title=t(guild_id, "adventure.battle.title", username=attacker.username, teamName=teamName),
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
            with getDbSession() as session2:
                playerRepo2 = PlayerRepository(session2)
                fresh_attacker = playerRepo2.getById(attacker_id)

                if battle.turn >= battle.maxturn:
                    result = t(guild_id, "adventure.result.result_draw")
                    outcome_text = t(guild_id, "adventure.result.outcome_draw")
                    thuong = t(guild_id, "adventure.result.reward_draw", reward=bonus_reward)
                elif battle.is_team_alive(battle.attacker_team):
                    result = t(guild_id, "adventure.result.result_win")
                    bonus_reward = random.randint(30000, 50000)
                    fresh_attacker.coin_balance += bonus_reward
                    outcome_text = t(guild_id, "adventure.result.outcome_win", teamName=teamName)
                    thuong = t(guild_id, "adventure.result.reward_win", reward=bonus_reward, teamName=teamName)
                else:
                    result = t(guild_id, "adventure.result.result_lose")
                    outcome_text = t(guild_id, "adventure.result.outcome_lose", teamName=teamName)
                    thuong = t(guild_id, "adventure.result.reward_lose", teamName=teamName)

                fresh_attacker.exp += 10
                session2.commit()

                result_embed = discord.Embed(
                    title=t(guild_id, "adventure.result.title", username=fresh_attacker.username, teamName=teamName),
                    description=(
                        f"{t(guild_id, 'adventure.result.line_result', result=result)}\n"
                        f"{thuong}\n\n"
                        f"{outcome_text}"
                    ),
                    color=discord.Color.green() if bonus_reward != 0 else discord.Color.red()
                )
                result_embed.set_footer(text=t(guild_id, "adventure.result.footer_rank", rankPoints=fresh_attacker.rank_points))
                await interaction.followup.send(embed=result_embed)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(
                t(guild_id, "adventure.error", trace=tb),
                ephemeral=True
            )

    @adventure.error
    async def buycard_error(self, interaction: discord.Interaction, error):
        guild_id = interaction.guild.id if interaction.guild else None

        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                t(guild_id, "adventure.cooldown", seconds=error.retry_after),
                ephemeral=True
            )
            return

        raise error


async def setup(bot):
    await bot.add_cog(Adventure(bot))
