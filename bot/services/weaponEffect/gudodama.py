
from bot.services.effectBase import Effect

class Gudodama(Effect):
    def __init__(self):
        super().__init__(
            name="unEffect",
            duration=2,
            effect_type="condition",
            value=None,
            flat_bonus=0,
            description="miễn hiệu ứng root, trong 2 turn"
        )

    def apply(self, card, target = None):
            logs = []
            self.duration -= 1
            logs.extend(f"{card.name} miễn nhiễm hiệu ứng từ vũ khí Gudodama còn {self.duration} lần")
            if self.duration == 0:
                card.passives.remove(self)
            return logs
