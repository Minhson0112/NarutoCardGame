from bot.services.cardBase import Card
from bot.services.effect.healOverTimeEffect import HealOverTimeEffect

class Orochimaru(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🧪 {self.name} sử dụng dược thuật điên, hồi phục sau mỗi turn!")

        # Tính lượng hồi 300% SMKK mỗi lượt
        heal_per_turn = int(self.get_effective_base_damage() * 3)
        hot_effect = HealOverTimeEffect(
            duration=5,
            value=heal_per_turn,
            description=f"Dược thuật điên của {self.name}"
        )
        self.effects.append(hot_effect)
        logs.append(
            f"💧 {self.name} sẽ hồi {heal_per_turn} HP mỗi lượt trong 5 lượt!"
        )

        return logs
