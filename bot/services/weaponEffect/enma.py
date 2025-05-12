
from bot.services.effectBase import Effect

class Enma(Effect):
    def __init__(self):
        super().__init__(
            name="lifeSteal",
            duration=None,
            effect_type="condition",
            value=None,
            flat_bonus=0,
            description="20% hút máu vĩnh viễn"
        )

