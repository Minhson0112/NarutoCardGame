from bot.services.effectBase import Effect

class RootEffect(Effect):
    def __init__(self, duration, description=""):
        super().__init__(
            name="Root",
            duration=duration,
            effect_type="debuff",
            value=None,  # Không cần giá trị cụ thể
            description=description
        )