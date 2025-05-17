from bot.services.cardBase import Card
from bot.services.effect.burnEffect import BurnEffect

class UchihaSasuke(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🔥 {self.name} thi triển Amaterasu, thiêu đốt hai kẻ địch tuyến sau!")

        # 100% sát thương cơ bản mỗi lượt
        burn_damage = int(self.get_effective_base_damage() * 1)
        # Lấy hai thành viên tuyến sau (chỉ số 1 và 2)
        targets = [c for c in self.enemyTeam[1:3] if c.is_alive()]

        # Fallback: nếu không có ai ở vị trí 1-2, lấy 1 target đầu tiên còn sống
        if not targets:
            first_alive = next((c for c in self.enemyTeam if c.is_alive()), None)
            targets = [first_alive] if first_alive else []

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
