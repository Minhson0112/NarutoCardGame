from bot.services.cardBase import Card
from bot.services.effect.reflectDamageEffect import ReflectDamageEffect

class Haku(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"❄️ {self.name} sử dụng Băng Thuật, ban tặng đồng minh khả năng phản sát thương!")

        # 70% phản damage trong 2 lượt cho toàn đội
        for ally in self.team:
            if ally.is_alive():
                reflect = ReflectDamageEffect(
                    duration=2,
                    reflect_percent=0.7,
                    description=f"Phản sát thương từ Băng Thuật của {self.name}"
                )
                ally.effects.append(reflect)
                logs.append(
                    f"🌀 {ally.name} nhận hiệu ứng phản damage 70% trong 2 lượt!"
                )

        return logs
