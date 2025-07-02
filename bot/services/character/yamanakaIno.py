from bot.services.cardBase import Card
from bot.services.effect.buffSpeedEffect import BuffSpeedEffect

class YamanakaIno(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("🌸 Ino đọc suy nghĩ kẻ địch ")
        # Tìm đồng minh đầu tiên còn sống (không phải bản thân)
        alive_allies = [c for c in self.team if c.is_alive()]
        
        if alive_allies:
            target = alive_allies[0]
            # Tạo buff speed
            buff_speed_effect = BuffSpeedEffect(
                duration=2,
                value=1.0,  # 100%
                description=f"né của {target.name} từ kỹ năng Ino"
            )
            target.effects.append(buff_speed_effect)
            logs.append(
                f"🌸 Ino đọc suy nghĩ địch tăng {int(buff_speed_effect.value * 100)}% speed trong {buff_speed_effect.duration} turn cho {target.name}."
            )
        else:
            logs.append("🌸 Ino không tìm thấy đồng minh nào để buff speed.")

        return logs