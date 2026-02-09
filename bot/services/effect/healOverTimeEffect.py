from bot.services.effectBase import Effect

class HealOverTimeEffect(Effect):
    def __init__(self, duration, value, description=""):
        """
        Args:
            duration (int): Số lượt hiệu ứng tồn tại.
            value (int): Số HP hồi mỗi lượt.
            description (str): Mô tả hiệu ứng.
        """
        super().__init__(
            name="HoT",
            duration=duration,
            effect_type="buff",
            value=value,
            flat_bonus=0,
            description=description
        )

    def apply(self, card):
        # Hồi máu mỗi lượt
        logs = []
        newLog = card.receive_healing(amount=self.value)
        logs.extend(newLog)
        return logs
