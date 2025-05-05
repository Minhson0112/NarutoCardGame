from bot.services.effectBase import Effect

class BuffArmorEffect(Effect):
    def __init__(self, duration, value, flat_bonus=0, description="Tăng giáp"):
        super().__init__(
            name="BuffArmor",
            duration=duration,
            effect_type="buff",
            value=value,
            flat_bonus=flat_bonus,
            description=description
        )
