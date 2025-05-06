from bot.services.cardBase import Card

class Jiraiya(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"📜 {self.name} thi triển Đại Chí Kim: càn quét toàn bộ kẻ địch bằng sát thương chuẩn!")

        # 800% sát thương cơ bản (bỏ qua giáp)
        damage = int(self.get_effective_base_damage() * 5)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            dealt, new_logs = target.receive_damage(
                damage,
                true_damage=True,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(new_logs)

        return logs
