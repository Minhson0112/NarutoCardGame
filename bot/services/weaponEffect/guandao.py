from bot.services.effectBase import Effect

class Guandao(Effect):
    def __init__(self):
        super().__init__(
            name="TrueDamage",
            duration=None,
            effect_type="BeforeBasicAttack",
            value=None,
            flat_bonus=0,
            description="đòn đánh thường sẽ kết liễu mục tiêu dới 3% máu"
        )
