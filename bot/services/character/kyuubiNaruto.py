from bot.services.cardBase import Card
from bot.services.effect.buffDamageEffect import BuffDamageEffect

class KyuubiNaruto(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🐺 {self.name} cuồng hóa ở dạng Vĩ Thú, tăng sức mạnh khủng khiếp và tấn công toàn đội địch!")

        # Buff sát thương +300% trong 3 lượt
        berserk = BuffDamageEffect(
            duration=3,
            value=2.0,  # +200% sát thương cơ bản
            description="Cuồng hóa Vĩ Thú của Naruto"
        )
        self.effects.append(berserk)
        logs.append(f"⚔️ {self.name} nhận buff +200% sát thương trong 3 lượt!")

        # Tấn công toàn bộ kẻ địch với 200% SMKK
        damage = int(self.get_effective_base_damage() * 2)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            dealt, new_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(new_logs)

        return logs
