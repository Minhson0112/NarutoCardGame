from bot.services.effectBase import Effect

class BuffSpeedEffect(Effect):
    def __init__(self, duration, value, flat_bonus=0, description=""):
        super().__init__(
            name="BuffSpeed",
            duration=duration,
            effect_type="buff",
            value=value,
            flat_bonus=flat_bonus,
            description=description
        )
