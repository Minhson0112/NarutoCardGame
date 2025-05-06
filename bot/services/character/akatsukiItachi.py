from bot.services.cardBase import Card
from bot.services.effect.illusionEffect import IllusionEffect

class AkatsukiItachi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌌 {self.name} thi triển Ảo Thuật Tối Thượng, khiến kẻ địch quay sang tấn công lẫn nhau trong 2 lượt!")

        # Lấy tất cả kẻ địch còn sống
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để sử dụng Ảo Thuật.")
            return logs

        # Áp dụng IllusionEffect cho mỗi kẻ địch
        for target in alive_enemies:
            illusion = IllusionEffect(
                duration=2,
                description=f"Ảo Thuật của {self.name}"
            )
            target.effects.append(illusion)
            logs.append(f"🎭 {target.name} bị Ảo Thuật, sẽ tấn công đồng đội trong 2 lượt!")

        return logs
