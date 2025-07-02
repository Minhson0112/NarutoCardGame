from bot.services.cardBase import Card

class InuzukaKiba(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🐶 {self.name} gọi chó tấn công toàn bộ đối phương bằng Fang Over Fang!")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.get_effective_base_damage() * 3)  # 300%

        for target in alive_enemies:
            dealt, new_logs = target.receive_damage(damage, true_damage=True, execute_threshold=None, attacker=self)
            logs.extend(new_logs)

        return logs