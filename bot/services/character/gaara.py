from bot.services.cardBase import Card
from bot.services.effect.buffArmorEffect import BuffArmorEffect

class Gaara(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("🏜️ Gaara thi triển Bình Phong Cát, gia tăng phòng thủ cho cả đội!")

        # 100% SMKK chuyển thành flat_bonus
        armor_buff_amount = int(self.get_effective_base_damage() * 1.0)

        # Áp dụng buff cho toàn bộ đồng minh còn sống
        for ally in self.team:
            if ally.is_alive():
                buff = BuffArmorEffect(
                    duration=5,
                    value=0,  # không dùng tỷ lệ %, dùng flat_bonus
                    flat_bonus=armor_buff_amount,
                    description="Phòng thủ tuyệt đối của Gaara"
                )
                ally.effects.append(buff)
                logs.append(
                    f"🛡️ {ally.name} nhận buff +{armor_buff_amount} giáp "
                    f"(100% SMKK) trong 2 lượt."
                )

        return logs
