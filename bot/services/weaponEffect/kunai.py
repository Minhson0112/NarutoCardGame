from bot.services.effectBase import Effect

class kunai(Effect):
    def __init__(self):
        super().__init__(
            name="ReviveCharka",
            duration=None,
            effect_type="AfterBasicAttack",
            value=None,
            flat_bonus=5,
            description="mỗi đòn đánh nhận 5 charka"
        )


    def apply(self, card, target = None):
        logs = []
        logs.extend(card.receive_chakra_buff(self.flat_bonus))
        return logs
