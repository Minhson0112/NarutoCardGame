import random

class Battle:
    def __init__(self, attacker_team, defender_team, maxturn):
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

    def get_default_target(self, enemy_team):
        for idx in range(3):  # hàng đầu -> giữa -> sau
            if enemy_team[idx].is_alive():
                return enemy_team[idx]
        return None

    def is_team_alive(self, team):
        return any(card.is_alive() for card in team)

    def increase_chakra(self, team):
        for card in team:
            if card.is_alive():
                card.chakra += 20

    def get_team_total_speed(self, team):
        return sum(card.speed for card in team if card.is_alive())

    def battle_turn_one_card(self, atk, enemy_team):
        logs = []
        if not atk.is_alive():
            return logs

        if atk.has_effect("Stun"):
            logs.append(f"⚡ {atk.name} đang bị khống chế, không thể hành động.")
            logs.extend(atk.process_effects())
            return logs

        if atk.chakra >= 100:
            logs.append(f"{atk.name} dùng kỹ năng đặc biệt!")
            logs += atk.special_skills()
            atk.chakra = 0
        else:
            tgt = atk.target if atk.target and atk.target.is_alive() else self.get_default_target(enemy_team)
            if not tgt:
                logs.append(f"{atk.name} không có mục tiêu.")
                return logs

            logs.append(f"**{atk.name}** tấn công **{tgt.name}**")
            if random.random() < tgt.speed:
                logs.append(f"→ {tgt.name} né thành công! ({tgt.speed:.0%})")
            else:
                crit = random.random() < atk.crit_rate
                crit = random.random() < atk.crit_rate
                dmg = atk.base_damage * (2 if crit else 1)
                dealt, new_logs = tgt.receive_damage(dmg)
                if crit:
                    logs.append(f"💥 ĐÒN CHÍ MẠNG của {atk.name}!")
                logs.extend(new_logs)
        logs.extend(atk.process_effects())
        atk.chakra += 20
        return logs