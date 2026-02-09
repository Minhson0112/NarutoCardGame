from bot.services.effectBase import Effect

class BuffCritEffect(Effect):
    def __init__(self, duration, value, flat_bonus=0, description=""):
        super().__init__(
            name="BuffCrit",
            duration=duration,
            effect_type="buff",
            value=value,
            flat_bonus=flat_bonus,
            description=description,
        )
