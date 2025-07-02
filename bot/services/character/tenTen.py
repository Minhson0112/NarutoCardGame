from bot.services.cardBase import Card

class TenTen(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"💥 {self.name} tung kỹ năng: Mưa vũ khí tấn công toàn bộ kẻ địch.")
        damage = int(self.get_effective_base_damage() * 2)

        # Gây damage toàn bộ địch còn sống
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        if not alive_enemies:
            logs.append("🎯 Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            dealt, new_logs = target.receive_damage(damage, true_damage=False, execute_threshold=None, attacker=self)
            logs.append(f"🎯 {self.name} ném vũ khí vào {target.name} gây {dealt} sát thương.")
            logs.extend(new_logs)

        return logs