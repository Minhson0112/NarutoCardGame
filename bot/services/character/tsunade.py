from bot.services.cardBase import Card
from bot.services.effect.buffArmorEffect import BuffArmorEffect

class Tsunade(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🐌 {self.name} gọi Sên Thần, triệu hồi Katsuyu để hỗ trợ đồng đội!")

        # Hồi máu cho toàn đội bằng 800% SMKK
        heal_amount = int(self.get_effective_base_damage() * 7)
        for ally in self.team:
            if ally.is_alive():
                logs.extend(ally.receive_healing(amount=heal_amount))

        # Buff giáp flat bằng 30% SMKK của Tsunade trong 5 lượt
        flat_bonus = int(self.get_effective_base_damage() * 0.3)
        for ally in self.team:
            if ally.is_alive():
                armor_buff = BuffArmorEffect(
                    duration=5,
                    value=0.0,                # không dùng % cơ bản
                    flat_bonus=flat_bonus,    # +30% SMKK
                    description=f"Giáp từ Katsuyu của {self.name}"
                )
                ally.effects.append(armor_buff)
                logs.append(
                    f"🛡️ {ally.name} nhận buff +{flat_bonus} giáp "
                    f"(30% SMKK của {self.name}) trong 5 lượt!"
                )

        return logs
