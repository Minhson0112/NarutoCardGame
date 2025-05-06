from bot.services.cardBase import Card
from bot.services.effect.burnEffect import BurnEffect

class TerumiMei(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌋 {self.name} phun dung nham nóng, thiêu đốt toàn bộ kẻ địch trong 3 lượt!")

        # 200% sát thương cơ bản làm giá trị burn mỗi lượt
        burn_damage = int(self.get_effective_base_damage() * 2)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để thiêu đốt.")
            return logs

        for target in alive_enemies:
            # Tạo hiệu ứng Burn trong 3 lượt
            burn_effect = BurnEffect(
                duration=3,
                value=burn_damage,
                description=f"Dung nham của {self.name}"
            )
            target.effects.append(burn_effect)
            logs.append(
                f"🔥 {target.name} chịu {burn_damage} sát thương mỗi lượt trong 3 lượt!"
            )

        return logs
