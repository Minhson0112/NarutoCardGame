from bot.services.effectBase import Effect

class DebuffDamageEffect(Effect):
    def __init__(self, duration, value, flat_bonus=0, description=""):
        """
        Hiệu ứng giảm sát thương:
        - value: % giảm (ví dụ 0.2 = -20%),
        - flat_bonus: trừ thêm trực tiếp (int).
        """
        super().__init__(
            name="DebuffDamage",
            duration=duration,
            effect_type="debuff",
            value=value,
            flat_bonus=flat_bonus,
            description=description
        )