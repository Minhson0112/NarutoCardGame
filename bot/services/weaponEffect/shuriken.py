from bot.services.effectBase import Effect

class Shuriken(Effect):
    def __init__(self):
        super().__init__(
            name="breakArmorEffect",
            duration=None,
            effect_type="AfterBasicAttack",
            value=None,
            flat_bonus=1,
            description="đòn đánh phá 1 giáp của đối phương."
        )

    def apply(self, card, target = None):
        logs = []
        if target and target.is_alive():
            logs.extend(target.reduce_armor_direct(armor_reduce=self.flat_bonus))
        return logs

