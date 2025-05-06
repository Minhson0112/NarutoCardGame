from bot.services.cardBase import Card
from bot.services.effect.immuneEffect import ImmuneEffect

class SenjuHashirama(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌳 {self.name} triệu hồi Phật Nghìn Mắt Nghìn Tay: hồi phục và bảo hộ toàn đội!")

        # 1️⃣ Hồi máu cho cả đội bằng 500% SMKK
        heal_amount = int(self.get_effective_base_damage() * 5)
        for ally in self.team:
            if ally.is_alive():
                logs.extend(ally.receive_healing(amount=heal_amount))

        # 2️⃣ Cấp hiệu ứng miễn nhiễm sát thương trong 2 lượt cho toàn đội
        for ally in self.team:
            if ally.is_alive():
                immune = ImmuneEffect(
                    duration=2,
                    description=f"Miễn nhiễm sát thương từ {self.name}"
                )
                ally.effects.append(immune)
                logs.append(f"🛡️ {ally.name} được miễn nhiễm sát thương trong 2 lượt!")

        return logs
