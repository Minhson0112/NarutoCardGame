from bot.services.effectBase import Effect

class DebuffCritEffect(Effect):
    def __init__(self, duration, value, flat_bonus=0, description="Giảm chí mạng"):
        super().__init__(
            name="DebuffCrit",
            duration=duration,
            effect_type="debuff",
            value=value,
            flat_bonus=flat_bonus,
            description=description
        )
