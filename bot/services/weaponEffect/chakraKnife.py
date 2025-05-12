from bot.services.effectBase import Effect
from bot.services.effect.rootEffect import RootEffect
import random

class ChakraKnife(Effect):
    def __init__(self):
        super().__init__(
            name="RootEffectOnBasicAttack",
            duration=None,
            effect_type="AfterBasicAttack",
            value=0.15,
            flat_bonus=0,
            description="đòn đánh có 15% câm lặng địch 1 turn"
        )

    def apply(self, card, target = None):
        logs = []
        if random.random() < self.value and target is not None:
            silence = RootEffect(
                duration=1,
                description=f"Câm lặng từ vũ khí ChakraKnife của {card.name}"
            )
            blocked = False
            for p in target.passives:
                if p.name == "unEffect":
                    logs.extend(p.apply(target))
                    blocked = True
                    break
            if not blocked:
                target.effects.append(silence)
                logs.append(f"🔪 {target.name} bị câm lặng 1 turn từ vũ khí ChakraKnife! (15%)")

        return logs
