from bot.services.effectBase import Effect

class knife(Effect):
    def __init__(self):
        super().__init__(
            name="ExecuteThreshold",
            duration=None,
            effect_type="BeforeBasicAttack",
            value=0.03,
            flat_bonus=0,
            description="đòn đánh thường sẽ kết liễu mục tiêu dới 3% máu"
        )
