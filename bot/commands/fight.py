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
from bot.services.i18n import t


class Fight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_fights: set[int] = set()

    @app_commands.command(name="fight", description="Thách đấu người chơi cùng trình độ")
    async def fight(self, interaction: discord.Interaction):
        attacker_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None

        if attacker_id in self.active_fights:
            await interaction.response.send_message(
                t(guild_id, "fight.already_in_fight"),
                ephemeral=True
            )
            return

        self.active_fights.add(attacker_id)
        await interaction.response.defer(thinking=True)

        try:
            with getDbSession() as session:
                playerRepo = PlayerRepository(session)
                cardRepo = PlayerCardRepository(session)
                weaponRepo = PlayerWeaponRepository(session)
                activeSetupRepo = PlayerActiveSetupRepository(session)

                attacker = playerRepo.getById(attacker_id)
                if not attacker:
                    await interaction.followup.send(t(guild_id, "fight.not_registered"))
                    return

                attackerSetup = activeSetupRepo.getByPlayerId(attacker_id)
                slots = [
                    attackerSetup.card_slot1,
                    attackerSetup.card_slot2,
                    attackerSetup.card_slot3,
                ]
                if any(slot is None for slot in slots):
                    await interaction.followup.send(t(guild_id, "fight.need_full_team"))
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
                    battle_attacker_team.append(create_card(*params, guild_id=guild_id))

                minRank = (attacker.rank_points or 0) - 30
                maxRank = (attacker.rank_points or 0) + 30
                opponents = session.query(Player).filter(
                    Player.player_id != attacker_id,
                    Player.rank_points >= minRank,
                    Player.rank_points <= maxRank
                ).all()

                valid_opponents = []
                for opp in opponents:
                    oppSetup = activeSetupRepo.getByPlayerId(opp.player_id)
                    if (
                        oppSetup
                        and oppSetup.card_slot1 is not None
                        and oppSetup.card_slot2 is not None
                        and oppSetup.card_slot3 is not None
                    ):
                        valid_opponents.append(opp)

                defender = None
                if valid_opponents:
                    defender = random.choice(valid_opponents)
                else:
                    top10 = playerRepo.getTop10()
                    top10 = [p for p in top10 if p.player_id != attacker_id]
                    top10_valid = []
                    for p in top10:
                        pSetup = activeSetupRepo.getByPlayerId(p.player_id)
                        if (
                            pSetup
                            and pSetup.card_slot1 is not None
                            and pSetup.card_slot2 is not None
                            and pSetup.card_slot3 is not None
                        ):
                            top10_valid.append(p)

                    if top10_valid:
                        attacker_ids = [p.player_id for p in playerRepo.getTop10()]
                        if attacker_id in attacker_ids and attacker_ids.index(attacker_id) == 0:
                            await interaction.followup.send(t(guild_id, "fight.top1_no_opponent"))
                            return
                        defender = random.choice(top10_valid)

                if defender is None:
                    await interaction.followup.send(t(guild_id, "fight.no_opponent"))
                    return

                defenderSetup = activeSetupRepo.getByPlayerId(defender.player_id)
                defender_slots = [
                    defenderSetup.card_slot1,
                    defenderSetup.card_slot2,
                    defenderSetup.card_slot3,
                ]
                defender_cards = [cardRepo.getById(cid) for cid in defender_slots]

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
                    battle_defender_team.append(create_card(*params, guild_id=guild_id))

                paths = []
                for pc in attacker_cards + defender_cards:
                    key = pc.template.image_url
                    img_path = CARD_IMAGE_LOCAL_PATH_MAP.get(key, NON_CARD_PATH)
                    paths.append(img_path)

                buffer = renderImageFight(
                    paths[0], paths[1], paths[2],
                    paths[3], paths[4], paths[5],
                    BG_FIGHT
                )
                filename = f"battle_{attacker_id}.png"
                battle_file = discord.File(buffer, filename=filename)

                for c in battle_attacker_team:
                    c.team = battle_attacker_team
                    c.enemyTeam = battle_defender_team

                for c in battle_defender_team:
                    c.team = battle_defender_team
                    c.enemyTeam = battle_attacker_team

                attack_label = f"**{t(guild_id, 'fight.team_attack')}**"
                defense_label = f"**{t(guild_id, 'fight.team_defense')}**"

                initial_desc = []
                initial_desc += render_team_status(battle_attacker_team, attack_label)
                initial_desc += render_team_status(battle_defender_team, defense_label)
                initial_desc.append("\n" + t(guild_id, "fight.battle.starting"))

                log_embed = discord.Embed(
                    title=t(
                        guild_id,
                        "fight.battle.title",
                        attacker=attacker.username,
                        defender=defender.username
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

                battle = Battle(battle_attacker_team, battle_defender_team, maxturn=120, guild_id=guild_id)
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
                            static_lines += render_team_status(battle_attacker_team, attack_label)
                            static_lines += render_team_status(battle_defender_team, defense_label)

                            desc = "\n".join(static_lines)
                            desc += "\n" + t(
                                guild_id,
                                "fight.battle.turn_header",
                                turn=battle.turn,
                                cardName=c.name
                            ) + "\n"
                            desc += "\n".join(logs)

                            edit_embed = discord.Embed(
                                title=t(
                                    guild_id,
                                    "fight.battle.title",
                                    attacker=attacker.username,
                                    defender=defender.username
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
            bonus_highest = 0

            with getDbSession() as session2:
                playerRepo2 = PlayerRepository(session2)
                dailyTaskRepo2 = DailyTaskRepository(session2)

                fresh_attacker = playerRepo2.getById(attacker_id)
                fresh_defender = playerRepo2.getById(defender.player_id)

                if battle.turn >= battle.maxturn:
                    result = t(guild_id, "fight.result.draw")
                    fresh_attacker.winning_streak = 0
                    outcome_text = t(guild_id, "fight.result.draw_outcome")
                elif battle.is_team_alive(battle.attacker_team):
                    dailyTaskRepo2.updateFightWin(fresh_attacker.player_id)

                    fresh_attacker.rank_points += 10
                    fresh_defender.rank_points = max(0, fresh_defender.rank_points - 5)

                    fresh_defender.winning_streak = 0
                    fresh_attacker.winning_streak += 1

                    bonus_reward = 500 * fresh_attacker.winning_streak
                    if fresh_attacker.rank_points > fresh_attacker.highest_rank_points:
                        bonus_highest = 5000
                        fresh_attacker.highest_rank_points = fresh_attacker.rank_points

                    fresh_attacker.coin_balance += bonus_reward + bonus_highest
                    result = t(guild_id, "fight.result.win")
                    outcome_text = t(
                        guild_id,
                        "fight.result.rank_change_win",
                        attacker=fresh_attacker.username,
                        defender=fresh_defender.username
                    )
                else:
                    fresh_attacker.rank_points = max(0, fresh_attacker.rank_points - 10)
                    fresh_defender.rank_points += 5

                    fresh_attacker.winning_streak = 0
                    result = t(guild_id, "fight.result.lose")
                    outcome_text = t(
                        guild_id,
                        "fight.result.rank_change_lose",
                        attacker=fresh_attacker.username,
                        defender=fresh_defender.username
                    )

                fresh_attacker.exp += 10
                session2.commit()

                total_reward = bonus_reward + bonus_highest

                result_embed = discord.Embed(
                    title=t(
                        guild_id,
                        "fight.result.title",
                        attacker=fresh_attacker.username,
                        defender=fresh_defender.username
                    ),
                    description=(
                        f"{t(guild_id, 'fight.result.line_result', result=result)}\n"
                        f"{t(guild_id, 'fight.result.line_reward', reward=total_reward)}\n"
                        f"{t(guild_id, 'fight.result.line_streak', streak=fresh_attacker.winning_streak)}\n"
                        f"{outcome_text}"
                    ),
                    color=discord.Color.green() if total_reward > 0 else discord.Color.red()
                )
                result_embed.set_footer(
                    text=t(
                        guild_id,
                        "fight.result.footer_rank",
                        rankPoints=fresh_attacker.rank_points
                    )
                )
                await interaction.followup.send(embed=result_embed)

        except Exception:
            tb = traceback.format_exc()
            await interaction.followup.send(
                t(guild_id, "fight.error", trace=tb),
                ephemeral=True
            )
        finally:
            self.active_fights.discard(attacker_id)


async def setup(bot):
    await bot.add_cog(Fight(bot))
