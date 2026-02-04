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
from bot.services.battle import Battle
from bot.services.fightRender import renderImageFight
from bot.services.help import get_battle_card_params, render_team_status
from bot.services.createCard import create_card
from bot.services.i18n import t


class FightWith(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_fights: set[int] = set()

    @app_commands.command(name="fightwith", description="Pk vui với người chơi đã tag (không cập nhật rank)")
    @app_commands.describe(target="Tag của người chơi bạn muốn pk")
    async def fightwith(self, interaction: discord.Interaction, target: discord.Member):
        attacker_id = interaction.user.id
        defender_id = target.id
        guild_id = interaction.guild.id if interaction.guild else None

        if attacker_id in self.active_fights:
            await interaction.response.send_message(
                t(guild_id, "fightwith.already_in_fight"),
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
                dailyTaskRepo = DailyTaskRepository(session)

                attacker = playerRepo.getById(attacker_id)
                if not attacker:
                    await interaction.followup.send(t(guild_id, "fightwith.not_registered"))
                    return

                if defender_id == attacker_id:
                    await interaction.followup.send(t(guild_id, "fightwith.cannot_self"))
                    return

                attackerSetup = activeSetupRepo.getByPlayerId(attacker_id)
                slots = [
                    attackerSetup.card_slot1,
                    attackerSetup.card_slot2,
                    attackerSetup.card_slot3,
                ]
                if any(slot is None for slot in slots):
                    await interaction.followup.send(t(guild_id, "fightwith.need_full_team"))
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
                    battle_attacker_team.append(create_card(*params))

                defender_player = playerRepo.getById(defender_id)
                if not defender_player:
                    await interaction.followup.send(t(guild_id, "fightwith.target_not_registered"))
                    return

                defenderSetup = activeSetupRepo.getByPlayerId(defender_player.player_id)
                if (
                    not defenderSetup
                    or any(slot is None for slot in (defenderSetup.card_slot1, defenderSetup.card_slot2, defenderSetup.card_slot3))
                ):
                    await interaction.followup.send(t(guild_id, "fightwith.target_not_ready"))
                    return

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
                    battle_defender_team.append(create_card(*params))

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

                attack_label = f"**{t(guild_id, 'fightwith.team_attack')}**"
                defense_label = f"**{t(guild_id, 'fightwith.team_defense')}**"

                initial_desc = []
                initial_desc += render_team_status(battle_attacker_team, attack_label)
                initial_desc += render_team_status(battle_defender_team, defense_label)
                initial_desc.append("\n" + t(guild_id, "fightwith.battle.starting"))

                log_embed = discord.Embed(
                    title=t(
                        guild_id,
                        "fightwith.battle.title",
                        attacker=attacker.username,
                        defender=defender_player.username
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
                            static_lines += render_team_status(battle_attacker_team, attack_label)
                            static_lines += render_team_status(battle_defender_team, defense_label)

                            desc = "\n".join(static_lines)
                            desc += "\n" + t(
                                guild_id,
                                "fightwith.battle.turn_header",
                                turn=battle.turn,
                                cardName=c.name
                            ) + "\n"
                            desc += "\n".join(logs)

                            edit_embed = discord.Embed(
                                title=t(
                                    guild_id,
                                    "fightwith.battle.title",
                                    attacker=attacker.username,
                                    defender=defender_player.username
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

                if battle.turn >= battle.maxturn:
                    result = t(guild_id, "fightwith.result.draw")
                    outcome_text = t(guild_id, "fightwith.result.draw_outcome")
                elif battle.is_team_alive(battle.attacker_team):
                    result = t(guild_id, "fightwith.result.win")
                    outcome_text = t(guild_id, "fightwith.result.no_rank_note")
                else:
                    result = t(guild_id, "fightwith.result.lose")
                    outcome_text = t(guild_id, "fightwith.result.no_rank_note")

                dailyTaskRepo.updateFightwith(attacker_id)
                session.commit()

                result_embed = discord.Embed(
                    title=t(
                        guild_id,
                        "fightwith.result.title",
                        attacker=attacker.username,
                        defender=defender_player.username
                    ),
                    description=(
                        f"{t(guild_id, 'fightwith.result.line_result', result=result)}\n"
                        f"{t(guild_id, 'fightwith.result.line_reward', reward=0)}\n"
                        f"{t(guild_id, 'fightwith.result.line_streak', streak=t(guild_id, 'fightwith.result.streak_unchanged'))}\n"
                        f"{outcome_text}"
                    ),
                    color=discord.Color.green() if result == t(guild_id, "fightwith.result.win") else discord.Color.red()
                )
                result_embed.set_footer(
                    text=t(
                        guild_id,
                        "fightwith.result.footer_rank",
                        rankPoints=attacker.rank_points
                    )
                )
                await interaction.followup.send(embed=result_embed)

        except Exception as e:
            print("❌ Lỗi khi xử lý fightwith:", e)
            await interaction.followup.send(t(guild_id, "fightwith.error_generic"))
        finally:
            self.active_fights.discard(attacker_id)


async def setup(bot):
    await bot.add_cog(FightWith(bot))
