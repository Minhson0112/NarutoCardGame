from bot.services.effectBase import Effect

class Samehada(Effect):
    def __init__(self):
        super().__init__(
            name="MaxHpDamageEffect",
            duration=None,
            effect_type="AfterBasicAttack",
            value=None,
            flat_bonus=5,
            description="đòn đánh thường làm mất 5 charka của đối phương"
        )

    def apply(self, card, target = None):
        logs = []
        if target and target.is_alive():
            logs.extend(target.reduce_chakra_direct(self.flat_bonus))
        return logs
