from bot.services.effectBase import Effect

class Katana(Effect):
    def __init__(self):
        super().__init__(
            name="MaxHpDamageEffect",
            duration=None,
            effect_type="AfterBasicAttack",
            value=0.01,
            flat_bonus=0,
            description="đòn đánh gây thêm sát thương bằng 1% máu tối đa của đối phương"
        )

    def apply(self, card, target = None):
        logs = []
        if target and target.is_alive():
            bonusDamage = int(target.max_health * self.value)
            dealt, dmg_logs = target.receive_damage(bonusDamage, true_damage=True, execute_threshold=None, attacker=card)
            logs.extend(dmg_logs)
            if dealt > 0:
                logs.append(
                    f"🔪 {target.name} nhận thêm {dealt} sát thương (1% max HP) từ ChakraKnife."
                )
        return logs
