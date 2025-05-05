from bot.services.effectBase import Effect

class StunEffect(Effect):
    def __init__(self, duration, description="Bị choáng"):
        """
        Hiệu ứng choáng (không thể hành động).

        Args:
            duration (int): Số lượt bị choáng.
            description (str): Mô tả (ví dụ: "Choáng của Madara", "Choáng do kỹ năng xyz"...)
        """
        super().__init__(
            name="Stun",
            duration=duration,
            effect_type="debuff",
            value=None,
            description=description
        )