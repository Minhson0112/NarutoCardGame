from bot.services.effectBase import Effect
from bot.services.effect.immuneEffect import ImmuneEffect
class Tansa(Effect):
    def __init__(self):
        super().__init__(
            name="protection",
            duration=None,
            effect_type="condition",
            value=None,
            flat_bonus=0,
            description="nếu chịu sát thương và chết, sẽ sống lại với 1 máu và nhận miễn thương 2 turn."
        )

    def apply(self, card, target = None):
        logs = []
        if not card.is_alive():
            card.health = 1
            immune = ImmuneEffect(
                    duration=2,
                    description=f"Miễn nhiễm sát thương từ vũ khí Tansa"
                )
            card.effects.append(immune)
            logs.append(f"🛡️ {card.name} được hồi sinh với 1 máu và Miễn nhiễm sát thương 2 turn từ vũ khí Tansa!")
            card.passives.remove(self)
        return logs

