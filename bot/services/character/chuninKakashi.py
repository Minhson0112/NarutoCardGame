from bot.services.cardBase import Card

class ChuninKakashi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"⚡️ {self.name} sử dụng Lôi Độn: Chidori Đột Phát!")

        # Tính sát thương chính: 600% SMKK
        primary_damage = int(self.get_effective_base_damage() * 6)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        # 1️⃣ Tấn công mục tiêu hàng đầu
        first = alive_enemies[0]
        dealt1, logs1 = first.receive_damage(
            primary_damage,
            true_damage=False,
            execute_threshold=None,
            attacker=self
        )
        logs.extend(logs1)

        # 2️⃣ Lan truyền sang mục tiêu thứ hai (nếu có) với 1/2 sát thương
        if len(alive_enemies) > 1:
            second = alive_enemies[1]
            splash_damage = primary_damage // 2
            logs.append(f"→ Chỉ số Chidori lan sang {second.name}, gây {splash_damage} sát thương.")
            dealt2, logs2 = second.receive_damage(
                splash_damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(logs2)

        return logs
