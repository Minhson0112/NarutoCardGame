from bot.services.cardBase import Card
from bot.services.effect.illusionEffect import IllusionEffect

class YuhiKurenai(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌸 {self.name} thi triển Ảo Thuật, khiến đối phương tấn công chính đồng minh!")

        # Xác định mục tiêu tuyến đầu (đầu tiên còn sống)
        target = next((c for c in self.enemyTeam if c.is_alive()), None)
        if not target:
            logs.append("❌ Không tìm thấy mục tiêu để áp dụng Ảo Thuật.")
            return logs

        # Cộng dồn hoặc khởi tạo IllusionEffect
        stack_turns = 2
        existing = next(
            (e for e in target.effects if isinstance(e, IllusionEffect)),
            None
        )
        if existing:
            existing.duration += stack_turns
            logs.append(
                f"🔄 Ảo Thuật trên {target.name} được cộng dồn thành "
                f"{existing.duration} lượt."
            )
        else:
            illusion = IllusionEffect(
                duration=stack_turns,
                description=f"Ảo Thuật của {self.name}"
            )
            target.effects.append(illusion)
            logs.append(
                f"🎭 {target.name} bị trúng Ảo Thuật trong {stack_turns} lượt "
                "và sẽ nhầm lẫn đồng minh với kẻ địch!"
            )

        return logs
