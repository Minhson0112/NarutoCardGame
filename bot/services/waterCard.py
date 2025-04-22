from bot.services.cardBase import Card

class WaterCard(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"{self.name} kích hoạt kỹ năng đặc biệt hệ Thủy! 💧")

        alive_allies = [c for c in self.team if c.is_alive()]

        # Tính sẵn các giá trị buff
        heal = int(self.base_damage * 5)
        armor_buff = int(self.base_damage * 0.05)
        damage_buff = int(self.base_damage * 0.2)

        if self.tier == "Genin":
            # Chọn đồng minh có tỉ lệ máu thấp nhất
            target = min(
                alive_allies,
                key=lambda c: c.health / c.max_health if c.max_health else 1,
                default=None
            )
            if target:
                target.health = min(target.health + heal, target.max_health)
                logs.append(f"👉 {target.name} được hồi {heal} máu!")

        elif self.tier == "Chunin":
            # Lấy 2 đồng minh có % máu thấp nhất
            targets = sorted(
                alive_allies,
                key=lambda c: c.health / c.max_health if c.max_health else 1
            )[:2]
            for target in targets:
                target.health = min(target.health + heal, target.max_health)
                logs.append(f"👉 {target.name} được hồi {heal} máu!")

        elif self.tier == "Jounin":
            # Tương tự Chunin nhưng thêm buff giáp
            targets = sorted(
                alive_allies,
                key=lambda c: c.health / c.max_health if c.max_health else 1
            )[:2]
            for target in targets:
                target.health = min(target.health + heal, target.max_health)
                target.armor += armor_buff
                logs.append(f"👉 {target.name} được hồi {heal} máu và buff {armor_buff} giáp!")


        elif self.tier == "Kage":
            for target in alive_allies:
                target.health = min(target.health + heal, target.max_health)
                target.armor += armor_buff
                logs.append(f"⚔️ {target.name} được hồi {heal} máu, buff {armor_buff} giáp!")

        elif self.tier == "Legendary":
            for target in alive_allies:
                target.health = min(target.health + heal, target.max_health)
                target.armor += armor_buff
                target.base_damage += damage_buff
                logs.append(
                    f"🌟 {target.name} được hồi {heal} máu, buff {armor_buff} giáp và tăng {damage_buff} damage!"
                )
        else:
            logs.append(f"{self.name} không có kỹ năng đặc biệt phù hợp.")

        return logs
