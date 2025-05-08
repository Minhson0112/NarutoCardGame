from bot.services.cardBase import Card
from bot.services.effect.deBuffDamageEffect import DebuffDamageEffect

class LucVi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🗡️ {self.name} 💣kích hoạt kỹ năng Bom vĩ thú! 💥 tấn công toàn bộ kẻ địch và giảm 1 nửa sát thương của chúng trong 4 turn")
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

            # Giảm sát thương cơ bản
            damage_debuff = DebuffDamageEffect(
                duration=4,
                value=0.5,
                description="Giảm sát thương từ bom vĩ thú"
            )
            target.effects.append(damage_debuff)
            logs.append(f"⚔️ {target.name} bị giảm 50% sát thương trong 4 lượt!")


        return logs