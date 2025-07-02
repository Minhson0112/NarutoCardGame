from bot.services.effectBase import Effect
import random
class Kibaku(Effect):
    def __init__(self):
        super().__init__(
            name="AoE",
            duration=None,
            effect_type="AfterBasicAttack",
            value=0.15,
            flat_bonus=0,
            description="đòn đánh có tỉ lệ 15% lan sang 2 đối phương đằng sau."
        )

    def apply(self, card, target = None):
        logs = []
        damage = card.get_effective_base_damage()
        if random.random() < self.value:
            backline = card.enemyTeam[1:3]
            targets = [c for c in backline if c.is_alive()]

            for tgt in targets:
                logs.append(f"🗡️ {tgt.name} dính {damage} damage từ vũ khí bùa nổ Kibaku của {card.name}!")
                dealt, new_logs = tgt.receive_damage(
                    damage,
                    true_damage=False,
                    execute_threshold=None,
                    attacker=card
                )
                logs.extend(new_logs)
        return logs

