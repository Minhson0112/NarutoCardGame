from bot.services.cardBase import Card
from bot.services.effect.illusionEffect import IllusionEffect

class UchihaItachi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌑 {self.name} thi triển Ảo Thuật Cực Mạnh, khiến hai kẻ địch hàng đầu tấn công đồng minh và chịu sát thương!")

        # 200% sát thương cơ bản của Itachi
        damage = int(self.get_effective_base_damage() * 2)
        # Lọc hai kẻ địch hàng đầu còn sống
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        front_two = alive_enemies[:2]

        if not front_two:
            logs.append("❌ Không có mục tiêu hàng đầu để áp dụng Ảo Thuật.")
            return logs

        for target in front_two:
            # Áp dụng IllusionEffect trong 2 lượt
            illusion = IllusionEffect(
                duration=2,
                description=f"Ảo Thuật của {self.name}"
            )
            target.effects.append(illusion)
            logs.append(f"🎭 {target.name} bị trúng Ảo Thuật trong 2 lượt và sẽ nhầm đồng minh thành kẻ địch!")

            # Gây sát thương thường
            dealt, dmg_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(dmg_logs)

        return logs
