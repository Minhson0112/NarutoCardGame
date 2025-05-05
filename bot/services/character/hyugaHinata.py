from bot.services.cardBase import Card
from bot.services.effect.buffArmorEffect import BuffArmorEffect

class HyugaHinata(Card):
    def special_skills(self):
        logs: list[str] = []

        logs.append("🛡️ Hinata thi triển Bát Quái Hồi Thiên, tăng cường phòng thủ!")

        # Tăng giáp bản thân: 100% sát thương cơ bản trong 3 lượt
        armor_value = 0  # Nếu không cần % tăng theo giáp hiện có
        flat_bonus = int(self.get_effective_base_damage() * 1.0)

        armor_buff = BuffArmorEffect(
            duration=3,
            value=armor_value,
            flat_bonus=flat_bonus,
            description="Hồi Thiên của Hinata"
        )
        self.effects.append(armor_buff)
        logs.append(f"🛡️ {self.name} nhận buff giáp +{flat_bonus} trong 3 lượt.")

        return logs
