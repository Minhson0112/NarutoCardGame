from bot.services.cardBase import Card

class SarutobiHiruzen(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🔗 {self.name} thi triển cấm thuật Phong Ấn : chém mạnh vào tuyến đầu địch!")

        # Xác định mục tiêu tuyến đầu còn sống
        target = next((c for c in self.enemyTeam if c.is_alive()), None)
        if not target:
            logs.append("❌ Không tìm thấy mục tiêu tuyến đầu để chém.")
            return logs

        # Tính sát thương: 30% máu tối đa của mục tiêu + 200% sát thương cơ bản
        percent_damage = int(target.max_health * 0.3)
        base_damage = int(self.get_effective_base_damage() * 2)
        total_damage = percent_damage + base_damage

        # Gây sát thương chuẩn và kết liễu nếu dưới 10% HP tối đa
        dealt, dmg_logs = target.receive_damage(
            total_damage,
            true_damage=True,
            execute_threshold=0.1,  # 10% HP tối đa
            attacker=self
        )
        logs.extend(dmg_logs)

        return logs
