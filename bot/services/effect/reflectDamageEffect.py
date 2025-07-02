from bot.services.effectBase import Effect

class ReflectDamageEffect(Effect):
    def __init__(self, duration, reflect_percent, description="Phản sát thương"):
        super().__init__(
            name="Reflect",
            duration=duration,
            effect_type="buff",
            value=reflect_percent,
            description=description
        )