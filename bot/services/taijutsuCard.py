from bot.services.cardBase import Card

class TaijutsuCard(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"{self.name} mở cổng chakra – kích hoạt thể thuật tối thượng! 🥋")

        # Xác định hệ số nhân theo tier
        multiplier = {
            "Genin": 1.5,
            "Chunin": 1.8,
            "Jounin": 2.2,
            "Kage": 2.5,
            "Legendary": 3.0
        }.get(self.tier, 1.0)

        # Lưu lại các chỉ số gốc để log
        stats_before = {
            "base_damage": self.base_damage,
            "armor":      self.armor,
            "crit_rate":  self.crit_rate,
            "speed":      self.speed,
            "health":     self.health
        }

        # Tăng toàn bộ chỉ số (trừ máu)
        self.base_damage = int(self.base_damage * multiplier)
        self.armor       = int(self.armor * multiplier)

        crit_bonus = {
            "Genin":     0.05,
            "Chunin":    0.10,
            "Jounin":    0.15,
            "Kage":      0.20,
            "Legendary": 0.25
        }.get(self.tier, 0)

        speed_bonus = crit_bonus  # Cùng tỉ lệ

        self.crit_rate = min(self.crit_rate + crit_bonus, 0.9)
        self.speed     = min(self.speed + speed_bonus, 0.9)

        # Hy sinh 10% máu hiện tại, nhưng còn tối thiểu 100 máu
        sacrifice = int(stats_before["health"] * 0.1)
        new_health = max(self.health - sacrifice, 100)
        actual_sacrifice = self.health - new_health
        self.health = new_health

        # Ghi log kết quả
        logs.append(f"💪 {self.name} đã tăng toàn bộ chỉ số lên gấp {multiplier} lần:")
        logs.append(f"    ➤ Sát thương: {stats_before['base_damage']} → {self.base_damage}")
        logs.append(f"    ➤ Giáp:       {stats_before['armor']}       → {self.armor}")
        logs.append(f"    ➤ Tỉ lệ chí mạng: {stats_before['crit_rate']:.2f} → {self.crit_rate:.2f}")
        logs.append(f"    ➤ Né tránh:      {stats_before['speed']:.2f} → {self.speed:.2f}")
        logs.append(f"❤ {self.name} hy sinh {actual_sacrifice} máu (10% hiện có), còn lại {self.health}")

        return logs
