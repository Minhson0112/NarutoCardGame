from bot.services.effectBase import Effect

class HealOverTimeEffect(Effect):
    def __init__(self, duration, value, description="Heal Over Time"):
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
        old_hp = card.health
        card.health = min(card.max_health, card.health + self.value)
        healed = card.health - old_hp
        if healed > 0:
            logs.append(f"💧 {card.name} hồi {healed} HP từ {self.description}.")
        return logs
