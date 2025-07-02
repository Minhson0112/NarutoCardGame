from bot.services.cardBase import Card
from bot.services.effect.reflectDamageEffect import ReflectDamageEffect
from bot.services.effect.buffDamageEffect import BuffDamageEffect

class Haku(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"❄️ {self.name} sử dụng Băng Thuật, ban tặng đồng minh khả năng phản sát thương!")
        damageBuff = int(self.get_effective_base_damage() * 0.5)

        # 70% phản damage trong 2 lượt cho toàn đội
        for ally in self.team:
            if ally.is_alive():
                reflect = ReflectDamageEffect(
                    duration=2,
                    reflect_percent=0.7,
                    description=f"Phản sát thương từ Băng Thuật của {self.name}"
                )
                ally.effects.append(reflect)
                berserk = BuffDamageEffect(
                    duration=2,
                    flat_bonus = damageBuff,
                    description="Tăng sát thương từ bang thuật của haku"
                )
                ally.effects.append(berserk)
                logs.append(
                    f"🌀 {ally.name} nhận hiệu ứng phản damage 70% và tăng {damageBuff} damage trong 2 lượt!"
                )

        return logs
