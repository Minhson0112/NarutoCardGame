from bot.services.cardBase import Card
from bot.services.effect.reflectDamageEffect import ReflectDamageEffect

class TamVi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🗡️ {self.name} 💣kích hoạt kỹ năng Bom vĩ thú! 💥 tấn công toàn bộ kẻ địch và kích hoạt hiệu ứng phản sát thương(70%) trong 5 turn")
        # Lấy tất cả kẻ địch còn sống
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.get_effective_base_damage() * 2)

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            # Gây sát thương
            dealt, dmg_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(dmg_logs)

        reflect = ReflectDamageEffect(
            duration=5,
            reflect_percent=0.7,
            description=f"Phản sát thương từ lớp giáp dày của {self.name}"
        )

        self.effects.append(reflect)
        logs.append(
            f"🌀 {self.name} nhận hiệu ứng phản damage 70% trong 5 lượt!"
        )

        return logs