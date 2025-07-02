from bot.services.effectBase import Effect

class Bow(Effect):
    def __init__(self):
        super().__init__(
            name="changeTarget",
            duration=None,
            effect_type="BeforeBasicAttack",
            value=None,
            flat_bonus=0,
            description="đòn đánh thường sẽ tấn công ưu tiên hàng sau -> giữa -> đầu"
        )
