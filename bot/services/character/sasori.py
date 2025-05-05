from bot.services.cardBase import Card
from bot.services.effect.deBuffArmorEffect import DebuffArmorEffect
from bot.services.effect.burnEffect import BurnEffect

class Sasori(Card):
    def special_skills(self):
        logs: list[str] = []
        # Thông báo chiêu thức
        logs.append(f"🕷️ {self.name} thi triển rối: tấn công hàng đầu, giảm giáp và gây Độc!")

        # 1️⃣ Xác định mục tiêu hàng đầu còn sống
        target = next((c for c in self.enemyTeam if c.is_alive()), None)
        if not target:
            logs.append("❌ Không tìm thấy mục tiêu hàng đầu để tấn công.")
            return logs

        # 2️⃣ Giảm 50% giáp trong 3 lượt
        armor_debuff = DebuffArmorEffect(
            duration=3,
            value=0.5,  # Giảm 50% giáp hiện tại
            description="Giảm giáp của Sasori"
        )
        target.effects.append(armor_debuff)
        logs.append(f"🛡️ {target.name} bị giảm 50% giáp trong 3 lượt.")

        # 3️⃣ Gây Độc: 300% sát thương cơ bản mỗi lượt trong 3 lượt
        burn_amount = int(self.get_effective_base_damage() * 3)
        burn_effect = BurnEffect(
            duration=3,
            value=burn_amount,
            description="Độc của Sasori"
        )
        target.effects.append(burn_effect)
        logs.append(f"🔥 {target.name} chịu {burn_amount} sát thương mỗi lượt trong 3 lượt.")

        return logs
