from bot.services.effectBase import Effect
import random

class Tessen(Effect):
    def __init__(self):
        super().__init__(
            name="charkaBuffOnBasicAttack",
            duration=None,
            effect_type="AfterBasicAttack",
            value=0.2,
            flat_bonus=40,
            description="đòn đánh có 20% nhận thêm 40 charka"
        )

    def apply(self, card, target = None):
        logs = []
        if random.random() < self.value:
            logs.extend(card.receive_chakra_buff(self.flat_bonus))
        return logs
