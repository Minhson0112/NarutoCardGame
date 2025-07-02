from bot.services.effectBase import Effect

class BuffDamageEffect(Effect):
    def __init__(self, duration, value = 0.0, flat_bonus=0, description="Tăng sát thương"):
        """
        Hiệu ứng tăng sát thương:
        - value: % tăng (ví dụ 0.2 = +20%),
        - flat_bonus: cộng thêm trực tiếp (int).
        """
        super().__init__(
            name="BuffDamage",
            duration=duration,
            effect_type="buff",
            value=value,
            flat_bonus=flat_bonus,
            description=description
        )