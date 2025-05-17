from bot.services.cardBase import Card
from bot.services.effect.buffSpeedEffect import BuffSpeedEffect

class RaikageIII(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"⚡️ {self.name} kích hoạt Quỷ Mã, tăng né lên tối đa và lao thẳng vào mục tiêu!")

        # 1️⃣ Tăng né lên 70% trong 4 turn
        speed_buff = BuffSpeedEffect(
            duration=4,
            value=0.7,  # +70% speed, sau đó get_effective_speed sẽ clamp max 0.7
            description="Quỷ Mã tăng né tối đa"
        )
        self.effects.append(speed_buff)
        logs.append(f"🏃 {self.name} tăng né lên 70% trong 2 lượt.")

        # 2️⃣ Tấn công tuyến đầu với 500% SMKK sát thương chuẩn
        damage = int(self.get_effective_base_damage() * 8)
        front = next((c for c in self.enemyTeam if c.is_alive()), None)
        if not front:
            logs.append("❌ Không tìm thấy mục tiêu tuyến đầu để tấn công.")
            return logs

        dealt, dmg_logs = front.receive_damage(
            damage,
            true_damage=True,
            execute_threshold=None,
            attacker=self
        )
        logs.extend(dmg_logs)

        return logs
