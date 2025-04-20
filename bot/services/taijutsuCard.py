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
            "armor": self.armor,
            "crit_rate": self.crit_rate,
            "speed": self.speed,
            "health": self.health
        }

        # Tăng toàn bộ chỉ số
        self.base_damage = int(self.base_damage * multiplier)
        self.armor = int(self.armor * multiplier)

        crit_bonus = {
            "Genin": 0.05,
            "Chunin": 0.10,
            "Jounin": 0.15,
            "Kage": 0.20,
            "Legendary": 0.25
        }.get(self.tier, 0)

        speed_bonus = crit_bonus  # Cùng tỷ lệ

        self.crit_rate = min(self.crit_rate + crit_bonus, 0.9)
        self.speed = min(self.speed + speed_bonus, 0.9)

        # Hồi máu 30% max HP
        heal = int(self.max_health * 0.2)
        self.health = min(self.health + heal, self.max_health)

        logs.append(f"💪 {self.name} đã tăng toàn bộ chỉ số lên gấp {multiplier} lần và hồi {heal} máu:")
        logs.append(f"    ➤ Máu: {stats_before['health']} → {self.health}")
        logs.append(f"    ➤ Sát thương: {stats_before['base_damage']} → {self.base_damage}")
        logs.append(f"    ➤ Giáp: {stats_before['armor']} → {self.armor}")
        logs.append(f"    ➤ Tỷ lệ chí mạng: {stats_before['crit_rate']:.2f} → {self.crit_rate:.2f}")
        logs.append(f"    ➤ Né tránh (speed): {stats_before['speed']:.2f} → {self.speed:.2f}")
        return logs
    