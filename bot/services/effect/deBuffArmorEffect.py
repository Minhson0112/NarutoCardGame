from bot.services.effectBase import Effect

class DebuffArmorEffect(Effect):
    def __init__(self, duration, value, flat_bonus=0, description="Giảm giáp"):
        super().__init__(
            name="DebuffArmor",
            duration=duration,
            effect_type="debuff",
            value=value,
            flat_bonus=flat_bonus,
            description=description
        )
