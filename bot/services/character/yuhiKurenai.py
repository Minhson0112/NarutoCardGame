from bot.services.cardBase import Card
from bot.services.effect.illusionEffect import IllusionEffect

class YuhiKurenai(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌸 {self.name} thi triển Ảo Thuật, khiến đối phương tấn công chính đồng minh!")

        # 1️⃣ Xác định mục tiêu tuyến đầu (đầu tiên còn sống)
        target = next((c for c in self.enemyTeam if c.is_alive()), None)

        if not target:
            logs.append("❌ Không tìm thấy mục tiêu để áp dụng Ảo Thuật.")
            return logs

        # 2️⃣ Tạo hiệu ứng Illusion 2 turn
        illusion = IllusionEffect(duration=2)
        target.effects.append(illusion)

        logs.append(f"🎭 {target.name} bị trúng Ảo Thuật và sẽ nhầm lẫn đồng minh với kẻ địch trong 2 lượt!")

        return logs