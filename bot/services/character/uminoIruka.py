from bot.services.cardBase import Card

class UminoIruka(Card):
    def special_skills(self):
        logs: list[str] = []
        damage = int(self.get_effective_base_damage() * 5)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        logs.append(f"🍥 {self.name} tung chiêu tấn công 2 kẻ địch đầu tiên!")

        targets = alive_enemies[:2]  # Lấy tối đa 2 mục tiêu đầu tiên còn sống
        if not targets:
            logs.append("❌ Không tìm thấy mục tiêu để tấn công.")
            return logs

        for tgt in targets:
            dealt, new_logs = tgt.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.append(f"⚔️ {self.name} tấn công {tgt.name} gây {dealt} sát thương!")
            logs.extend(new_logs)

        return logs