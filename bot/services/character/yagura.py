from bot.services.cardBase import Card
from bot.services.effect.buffArmorEffect import BuffArmorEffect
from bot.services.effect.buffSpeedEffect import BuffSpeedEffect

class Yagura(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌊 Yagura kích hoạt tuyệt kỹ: Tăng giáp và né tránh!")

        yagura_damage = self.get_effective_base_damage()

        # 1️⃣ Buff giáp: 50% SMKK trong 4 turn
        armor_buff = BuffArmorEffect(
            duration=4,
            value=0,  # % tăng thêm (0  dùng flat_bonus)
            flat_bonus=int(yagura_damage * 0.5),
            description="Giáp tăng cường của Yagura"
        )
        self.effects.append(armor_buff)
        logs.append(f"🛡️ {self.name} tăng giáp bằng {int(yagura_damage/2)} trong 4 lượt.")

        # 2️⃣ Buff né: +30% trong 4 turn
        speed_buff = BuffSpeedEffect(
            duration=4,
            value=0.3,
            description="Né tránh tăng cường của Yagura"
        )
        self.effects.append(speed_buff)
        logs.append(f"🏃 {self.name} tăng né tránh thêm 30% trong 4 lượt.")

        return logs
