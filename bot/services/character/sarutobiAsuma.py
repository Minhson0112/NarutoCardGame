from bot.services.cardBase import Card

class SarutobiAsuma(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🍃 {self.name} thi triển Phong Thuật: càn quét toàn bộ kẻ địch!")

        # Tính sát thương và giáp cần phá
        asuma_damage = int(self.get_effective_base_damage() * 3)
        armor_break_amount = int(self.get_effective_base_damage() * 0.05)  # 5% smkk

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có mục tiêu nào để tấn công.")
            return logs

        for target in alive_enemies:
            # 1️⃣ Gây sát thương chuẩn
            dealt, dmg_logs = target.receive_damage(
                asuma_damage,
                true_damage=True,
                execute_threshold=0.05,  # 5% máu tối đa thì kết liễu
                attacker=self
            )
            logs.extend(dmg_logs)

            # 2️⃣ Giảm giáp vĩnh viễn (5% smkk)
            if armor_break_amount > 0:
                armor_logs = target.reduce_armor_direct(armor_reduce=armor_break_amount)
                logs.extend(armor_logs)

        return logs
