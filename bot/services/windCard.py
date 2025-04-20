from bot.services.cardBase import Card

class WindCard(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"{self.name} kích hoạt kỹ năng đặc biệt hệ Phong! 🌪️")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        # Ngưỡng máu tối đa để kết liễu theo tier
        finisher_threshold = {
            "Genin": 0.05,
            "Chunin": 0.10,
            "Jounin": 0.15,
            "Kage": 0.20,
            "Legendary": 0.25
        }.get(self.tier, 0)

        base_damage = self.base_damage * 3
        damage_reduction_rate = 0.8  # Mỗi mục tiêu sau sẽ giảm 20% damage

        for idx, target in enumerate(alive_enemies):
            multiplier = damage_reduction_rate ** idx
            damage = int(base_damage * multiplier)

            # Gây sát thương bình thường
            dealt = max(damage - target.armor, 0)
            target.health -= dealt

            if target.health < 0:
                target.health = 0

            logs.append(f"💨 {target.name} nhận {dealt} sát thương từ chiêu thức gió (giảm {int((1 - multiplier) * 100)}%).")

            # Sau khi nhận sát thương, kiểm tra ngưỡng máu kết liễu
            threshold_value = int(target.max_health * finisher_threshold)
            if target.health > 0 and target.health <= threshold_value:
                logs.append(f"⚡ {target.name} bị kết liễu ngay sau đòn đánh vì máu còn {target.health}/{target.max_health} (< {int(finisher_threshold * 100)}%)!")
                target.health = 0
                
        return logs
