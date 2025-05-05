from bot.services.cardBase import Card

class Deidara(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("💥 Deidara tạo vụ nổ lớn, nhắm vào tuyến đầu đối phương!")

        # 1️⃣ Xác định mục tiêu tuyến đầu còn sống
        target = next((c for c in self.enemyTeam if c.is_alive()), None)
        if not target:
            logs.append("❌ Không tìm thấy mục tiêu để tấn công.")
            return logs

        # 2️⃣ Gây 600% sát thương chuẩn (bỏ qua giáp)
        damage = int(self.get_effective_base_damage() * 6)
        dealt, new_logs = target.receive_damage(
            damage,
            true_damage=True,
            execute_threshold=None,
            attacker=self
        )
        logs.extend(new_logs)

        return logs
