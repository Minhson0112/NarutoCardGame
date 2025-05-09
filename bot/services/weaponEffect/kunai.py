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
        card.chakra += self.flat_bonus
        logs.append(f"🔪 {card.name} nhận +{self.flat_bonus} chakra từ Kunai!")
        return logs
