from bot.services.effectBase import Effect
from bot.services.effect.reflectDamageEffect import ReflectDamageEffect
import random

class Sansaju(Effect):
    def __init__(self):
        super().__init__(
            name="ReflectDamageEffect",
            duration=1,
            effect_type="AfterBasicAttack",
            value=0.4,
            flat_bonus=0,
            description="đòn đánh có 40% tỉ lệ cho phản 100% sát thương trong 1 turn"
        )

    def apply(self, card, target = None):
        logs = []
        if random.random() < self.value:
            reflect_effect = ReflectDamageEffect(
            duration=3,
            reflect_percent=0.7,
            description=f"Phản sát thương từ vũ khí Sansaju của {card.name}"
            )
            card.effects.append(reflect_effect)
            logs.append(f"{card.name} nhận được hiệu ứng phản 100% sát thương trong turn tới từ vũ khí Sansaju.")
        return logs
