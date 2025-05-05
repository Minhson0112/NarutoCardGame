from bot.services.cardBase import Card
from bot.services.effect.reflectDamageEffect import ReflectDamageEffect

class Kimimaro(Card):
    def special_skills(self):
        logs: list[str] = []
        
        logs.append(f"🦴 {self.name} kích hoạt Bát Vũ Thuật: hồi máu và tạo phản sát thương!")

        # 1️⃣ Hồi lại máu bằng 400% SMKK
        heal_amount = int(self.get_effective_base_damage() * 4)
        heal_logs = self.receive_healing(amount=heal_amount)
        logs.extend(heal_logs)

        # 2️⃣ Phản lại 40% damage trong 2 turn
        reflect_effect = ReflectDamageEffect(
            duration=2,
            reflect_percent=0.4,
            description=f"Hiệu ứng phản sát thương"
        )
        self.effects.append(reflect_effect)
        logs.append(f"🌀 {self.name} nhận hiệu ứng phản sát thương: phản lại 40% damage trong 2 lượt.")

        return logs
