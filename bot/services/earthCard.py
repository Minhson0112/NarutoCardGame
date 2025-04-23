from bot.services.cardBase import Card

class EarthCard(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"{self.name} kích hoạt kỹ năng đặc biệt hệ Thổ! 🪨")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        base_damage = self.base_damage
        damage_multiplier = 2 if self.tier == "Legendary" else 1
        dealt_damage = int(base_damage * damage_multiplier)

        for target in alive_enemies:
            # Gây sát thương hiện tại
            damage = max(dealt_damage - target.armor, 0)
            target.health -= damage
            if target.health < 0:
                target.health = 0

            # Giảm sát thương cơ bản
            original_base = target.base_damage
            target.base_damage = max(1, int(target.base_damage * 0.85))  # Không cho về 0

            logs.append(f"🪨 {target.name} bị tấn công: -{damage} HP, base_damage: {original_base} → {target.base_damage}")

            # Giảm crit rate (từ Chunin trở lên)
            if self.tier in ["Chunin", "Jounin", "Kage", "Legendary"]:
                original_crit = target.crit_rate
                target.crit_rate = max(0.0, target.crit_rate / 2)
                logs.append(f", crit_rate: {original_crit:.2f} → {target.crit_rate:.2f}")

            # Giảm speed (từ Jounin trở lên)
            if self.tier in ["Jounin", "Kage", "Legendary"]:
                original_speed = target.speed
                target.speed = max(0.0, target.speed * 0.85)
                logs.append(f", speed: {original_speed:.2f} → {target.speed:.2f}")

            # Giảm chakra (từ Kage trở lên)
            if self.tier in ["Kage", "Legendary"]:
                original_chakra = target.chakra
                target.chakra = max(0, target.chakra - 20)
                logs.append(f", chakra: {original_chakra} → {target.chakra}")
                
        return logs

