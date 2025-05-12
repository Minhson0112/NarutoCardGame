
from bot.services.effectBase import Effect

class Rinnegan(Effect):
    def __init__(self):
        super().__init__(
            name="unStun",
            duration=2,
            effect_type="condition",
            value=None,
            flat_bonus=0,
            description="miễn hiệu ứng choáng 2 turn"
        )

    def apply(self, card, target = None):
            logs = []
            self.duration -= 1
            logs.extend(f"{card.name} miễn nhiễm hiệu ứng từ vũ khí rinegan còn {self.duration} lần")
            if self.duration == 0:
                card.passives.remove(self)
            return logs
