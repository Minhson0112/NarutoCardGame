from bot.services.cardBase import Card
from bot.services.effect.reflectDamageEffect import ReflectDamageEffect

class Hidan(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"☠️ {self.name} thi triển nguyền rủa: phản lại 70% damage trong 3 lượt!")

        reflect_effect = ReflectDamageEffect(
            duration=3,
            reflect_percent=0.7,
            description=f"Phản sát thương từ nguyền rủa của {self.name}"
        )
        self.effects.append(reflect_effect)
        logs.append(f"🔮 {self.name} nhận hiệu ứng phản damage: phản lại 70% sát thương trong 3 lượt.")

        return logs