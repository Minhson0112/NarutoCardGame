from bot.services.cardBase import Card
from bot.services.effect.burnEffect import BurnEffect

class UchihaSasuke(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🔥 {self.name} thi triển Amaterasu, thiêu đốt hai kẻ địch tuyến sau!")

        # 200% sát thương cơ bản mỗi lượt
        burn_damage = int(self.get_effective_base_damage() * 2)
        # Lấy hai thành viên tuyến sau (chỉ số 1 và 2)
        targets = [c for c in self.enemyTeam[1:3] if c.is_alive()]

        if not targets:
            targets = next((c for c in self.enemyTeam if c.is_alive()), None)

        for target in targets:
            # Áp dụng hiệu ứng Burn trong 4 lượt
            burn = BurnEffect(
                duration=4,
                value=burn_damage,
                description=f"Amaterasu của {self.name}"
            )
            target.effects.append(burn)
            logs.append(
                f"🔥 {target.name} bị thiêu đốt bởi Amaterasu trong 4 lượt, chịu {burn_damage} sát thương mỗi lượt!"
            )

        return logs
