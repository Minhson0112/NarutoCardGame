from bot.services.cardBase import Card
from bot.services.effect.stunEffect import StunEffect

class KillerBee(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"💣 {self.name} kích hoạt Bom Vĩ Thú, tấn công toàn đội địch và gây choáng!")

        # Tính 200% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 2)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        # Gây sát thương và áp dụng choáng 1 lượt
        for target in alive_enemies:
            dealt, new_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(new_logs)
            stun_effect = StunEffect(
                duration=1,
                description="Choáng từ Bom Vĩ Thú của Killer Bee"
            )
            target.effects.append(stun_effect)
            logs.append(f"⚡ {target.name} bị choáng 1 lượt!")

        return logs
