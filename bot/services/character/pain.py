from bot.services.cardBase import Card
from bot.services.effect.debuffSpeedEffect import DebuffSpeedEffect

class Pain(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("☯️ Pain thi triển Thần La Thiên Trinh: tấn công và giảm tốc toàn bộ kẻ địch!")

        # 500% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 5)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            # Gây sát thương
            dealt, new_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(new_logs)

            # Giảm tốc 100% trong 3 turn
            speed_debuff = DebuffSpeedEffect(
                duration=3,
                value=1.0,
                description="Giảm tốc từ Thần La Tiến Trình"
            )
            target.effects.append(speed_debuff)
            logs.append(f"🐢 {target.name} bị giảm tốc 100% trong 3 lượt!")

        return logs
