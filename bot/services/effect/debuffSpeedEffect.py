from bot.services.effectBase import Effect

class DebuffSpeedEffect(Effect):
    def __init__(self, duration, value, flat_bonus=0, description="Giảm tốc độ"):
        super().__init__(
            name="DebuffSpeed",
            duration=duration,
            effect_type="debuff",
            value=value,
            flat_bonus=flat_bonus,
            description=description
        )
