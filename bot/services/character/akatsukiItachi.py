from bot.services.cardBase import Card
from bot.services.effect.illusionEffect import IllusionEffect

class AkatsukiItachi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌌 {self.name} thi triển Ảo Thuật Tối Thượng, khiến kẻ địch quay sang tấn công lẫn nhau trong 2 lượt!")

        # Lấy tất cả kẻ địch còn sống
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để sử dụng Ảo Thuật.")
            return logs

        # Áp dụng (và cộng dồn) IllusionEffect cho mỗi kẻ địch
        for target in alive_enemies:
            stack_turns = 2
            existing = next((e for e in target.effects if isinstance(e, IllusionEffect)), None)

            if existing:
                existing.duration += stack_turns
                logs.append(f"🔄 Ảo Thuật trên {target.name} được cộng dồn thành {existing.duration} lượt.")
            else:
                illusion = IllusionEffect(
                    duration=stack_turns,
                    description=f"Ảo Thuật của {self.name}"
                )
                target.effects.append(illusion)
                logs.append(f"🎭 {target.name} bị Ảo Thuật trong {stack_turns} lượt và sẽ tấn công đồng đội!")

        return logs
