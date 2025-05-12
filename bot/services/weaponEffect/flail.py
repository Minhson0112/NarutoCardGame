from bot.services.effectBase import Effect
from bot.services.effect.stunEffect import StunEffect
import random

class Flail(Effect):
    def __init__(self):
        super().__init__(
            name="RootEffectOnBasicAttack",
            duration=None,
            effect_type="AfterBasicAttack",
            value=None,
            flat_bonus=1,
            description="đòn đánh có 15% choáng địch 1 turn"
        )

    def apply(self, card, target = None):
        logs = []
        if random.random() < self.value and target is not None:
            stun_effect = StunEffect(
                    duration=self.flat_bonus,
                    description=f"Choáng từ vũ khí Flail của {card.name}"
                )
            blocked = False
            for p in target.passives:
                if p.name == "unStun":
                    logs.extend(p.apply(target))
                    blocked = True
                    break
            if not blocked:
                target.effects.append(stun_effect)
                logs.append(f"⚡ {target.name} bị choáng {self.flat_bonus} lượt từ vũ khí Flail của {card.name}.")

        return logs
