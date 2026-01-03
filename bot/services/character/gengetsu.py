from bot.services.cardBase import Card
from bot.services.effect.deBuffArmorEffect import DebuffArmorEffect

class Gengetsu(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌊 {self.name} sử dụng Thủy Độn đâm xuyênxuyên, nhắm vào tuyến đầu địch!")

        # Xác định mục tiêu tuyến đầu còn sống
        target = next((c for c in self.enemyTeam if c.is_alive()), None)
        if not target:
            logs.append("❌ Không tìm thấy mục tiêu tuyến đầu để tấn công.")
            return logs

        # Gây 300% sát thương chuẩn (bỏ qua giáp)
        damage = int(self.get_effective_base_damage() * 3)
        dealt, dmg_logs = target.receive_damage(
            damage,
            true_damage=True,
            execute_threshold=None,
            attacker=self
        )
        logs.extend(dmg_logs)

        # Giảm 50% giáp trong 2 lượt
        armor_debuff = DebuffArmorEffect(
            duration=2,
            value=0.5,  # giảm 50% giáp hiện tại
            description="Giảm giáp Thủy Độn của Gengetsu"
        )
        target.effects.append(armor_debuff)
        logs.append(f"🛡️ {target.name} bị giảm 50% giáp trong 2 lượt!")

        return logs
