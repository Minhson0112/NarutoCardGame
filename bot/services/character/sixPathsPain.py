from bot.services.cardBase import Card
from bot.services.effect.stunEffect import StunEffect

class SixPathsPain(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("☯️ Six Paths Pain tung ra Thần La Thiên Trinh Cực Mạnh: gây 700% SMKK, kết liễu nếu dưới 25% HP và choáng 1 lượt!")

        # 700% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 5)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            # Gây sát thương và kết liễu nếu dưới 25% HP tối đa
            dealt, new_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=0.25,  # 25% HP tối đa
                attacker=self
            )
            logs.extend(new_logs)

            # Áp dụng choáng 1 lượt
            stun = StunEffect(
                duration=1,
                description=f"Choáng từ Thần La Thiên Trinh của {self.name}"
            )
            target.effects.append(stun)
            logs.append(f"⚡ {target.name} bị choáng 1 lượt!")

        return logs
