from bot.services.cardBase import Card
from bot.services.effect.deBuffArmorEffect import DebuffArmorEffect

class Temari(Card):
    def special_skills(self):
        logs: list[str] = []

        logs.append("🌪️ Temari vung quạt thi triển Phong Thuật!")

        # Xác định mục tiêu: tướng đầu tiên còn sống
        tgt = next((c for c in self.enemyTeam if c.is_alive()), None)
        if not tgt:
            logs.append("❌ Không tìm thấy mục tiêu để tấn công.")
            return logs

        # Gây 500% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 5.0)
        dealt, new_logs = tgt.receive_damage(damage, true_damage=False, execute_threshold=None, attacker=self)
        logs.extend(new_logs)

        # Áp hiệu ứng giảm giáp 30% trong 2 lượt
        debuff = DebuffArmorEffect(
            duration=2,
            value=0.3,  # Giảm 30% giáp
            flat_bonus=0,
            description="Phong Thuật của Temari"
        )
        tgt.effects.append(debuff)
        logs.append(f"🌪️ {tgt.name} bị giảm 30% giáp trong 2 lượt.")

        return logs