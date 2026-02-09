import random
from bot.services.cardBase import Card
from bot.services.i18n import t


class Battle:
    def __init__(self, attacker_team, defender_team, maxturn, guild_id=None):
        self.attacker_team = attacker_team
        self.defender_team = defender_team
        self.first_team, self.second_team = (
            (attacker_team, defender_team)
            if self.get_team_total_speed(attacker_team) >= self.get_team_total_speed(defender_team)
            else (defender_team, attacker_team)
        )
        self.maxturn = maxturn
        self.winteam = None
        self.lostteam = None
        self.turn = 1
        self.logs = []
        self.guild_id = guild_id

    def get_default_target(self, enemy_team):
        for target in enemy_team:
            if target.is_alive():
                return target
        return None

    def get_default_target_reversed(self, enemy_team):
        for target in reversed(enemy_team):
            if target.is_alive():
                return target
        return None

    def is_team_alive(self, team):
        return any(card.is_alive() for card in team)

    def increase_chakra(self, team):
        for card in team:
            if card.is_alive():
                card.chakra += 20

    def get_team_total_speed(self, team):
        return sum(card.speed for card in team if card.is_alive())

    def battle_turn_one_card(self, atk: Card):
        logs = []

        guild_id = getattr(atk, "guild_id", None) or self.guild_id

        true_damage = False
        execute_threshold = None

        if atk.has_passives_effect("TrueDamage"):
            true_damage = True

        if atk.has_passives_effect("ExecuteThreshold"):
            execute_threshold = 0.03

        if atk.has_passives_effect("changeTarget"):
            atk.target = self.get_default_target_reversed(atk.enemyTeam)

        logs.extend(atk.process_pre_action_effects())

        if atk.has_effect("Stun"):
            logs.append(t(guild_id, "battle.controlled_skip_action").format(name=atk.name))
            logs.extend(atk.process_effects())
            return logs

        is_rooted = atk.has_effect("Root")

        if atk.chakra >= 100 and not is_rooted:
            logs.append(t(guild_id, "battle.special_use").format(name=atk.name))
            logs += atk.special_skills()
            atk.chakra = max(atk.chakra - 100, 0)
        else:
            if atk.chakra >= 100 and is_rooted:
                logs.append(t(guild_id, "battle.controlled_cant_use_special").format(name=atk.name))

            tgt = atk.target if atk.target and atk.target.is_alive() else self.get_default_target(atk.enemyTeam)
            if not tgt:
                logs.append(t(guild_id, "battle.no_target").format(name=atk.name))
                return logs

            logs.append(
                t(guild_id, "battle.basic_attack").format(attacker=atk.name, target=tgt.name)
            )

            if random.random() < tgt.get_effective_speed():
                logs.append(
                    t(guild_id, "battle.dodge_success").format(target=tgt.name, speed=tgt.speed)
                )
            else:
                crit = random.random() < atk.get_effective_crit_rate()
                dmg = atk.get_effective_base_damage() * (2 if crit else 1)
                dealt, new_logs = tgt.receive_damage(dmg, true_damage, execute_threshold, attacker=atk)

                if crit:
                    logs.append(t(guild_id, "battle.critical_hit").format(attacker=atk.name))

                logs.extend(new_logs)

            for e in atk.passives:
                if e.effect_type == "AfterBasicAttack":
                    logs.extend(e.apply(atk, tgt))

        logs.extend(atk.process_effects())
        logs.extend(atk.receive_chakra_buff(20))
        return logs
