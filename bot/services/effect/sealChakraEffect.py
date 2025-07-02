from bot.services.effectBase import Effect

class SealChakraEffect(Effect):
    def __init__(self, duration, description="Phong ấn chakra"):
        super().__init__(
            name="SealChakra",
            duration=duration,
            effect_type="debuff",
            value=None,
            flat_bonus=0,
            description=description
        )

    def apply(self, card):
        # Mỗi lượt vẫn tồn tại, nhưng không cho phép nhận chakra
        return [f"🔒 {card.name} bị phong ấn chakra, không thể tích tụ năng lượng."]

    def on_expire(self, card):
        # Khi hết hiệu lực, thông báo mở phong ấn
        return [f"⏳ {self.description} trên {card.name} đã hết hiệu lực, chakra có thể tăng trở lại."]
