from bot.services.effectBase import Effect

class ImmuneEffect(Effect):
    def __init__(self, duration, description="Miễn nhiễm sát thương"):
        super().__init__(
            name="Immune",
            duration=duration,
            effect_type="buff",
            value=None,
            description=description
        )