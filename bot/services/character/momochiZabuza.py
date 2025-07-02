from bot.services.cardBase import Card
from bot.services.effect.buffSpeedEffect import BuffSpeedEffect

class MomochiZabuza(Card):
    def special_skills(self):
        logs: list[str] = []

        # Tạo log thông báo kỹ năng
        logs.append(f"🌫️ {self.name} tạo sương mù, tăng né tránh cho toàn bộ đồng minh 20% trong 2 lượt!")

        # Tạo effect: tăng speed 20% (0.2) trong 2 turn
        effect = BuffSpeedEffect(
            duration=2,
            value=0.2,
            description="Sương mù của Zabuza"
        )

        # Buff cho toàn bộ đồng minh còn sống
        for teammate in self.team:
            if teammate.is_alive():
                teammate.effects.append(effect)
                logs.append(f"✅ {teammate.name} được buff né tránh.")

        return logs