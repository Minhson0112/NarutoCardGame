from bot.services.cardBase import Card
from bot.services.effect.buffArmorEffect import BuffArmorEffect

class Kakuzu(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"❤️ Kakuzu có 4 trái tim, hồi phục và gia tăng phòng thủ!")

        # Hồi lại 300% SMKK
        heal_amount = int(self.get_effective_base_damage() * 500)
        heal_logs = self.receive_healing(amount=heal_amount)
        logs.extend(heal_logs)

        # Tăng giáp bằng 100% SMKK trong 4 turn
        armor_buff_amount = int(self.get_effective_base_damage() * 1.0)
        armor_buff = BuffArmorEffect(
            duration=4,
            value=0,  # không dùng % giáp hiện tại
            flat_bonus=armor_buff_amount,
            description="Giáp từ 4 trái tim của Kakuzu"
        )
        self.effects.append(armor_buff)
        logs.append(f"🛡️ {self.name} nhận buff +{armor_buff_amount} giáp trong 4 lượt.")

        return logs
