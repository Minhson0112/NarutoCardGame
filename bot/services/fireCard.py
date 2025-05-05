from bot.services.cardBase import Card
from bot.services.effectBase import Effect
class FireCard(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"{self.name} kích hoạt kỹ năng đặc biệt hệ Hỏa! 🔥")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.get_effective_base_damage * 5)
        
        if self.tier == "Genin":
            # Tấn công hàng đầu tiên còn sống
            for i in range(3):
                if self.enemyTeam[i].is_alive():
                    target = self.enemyTeam[i]
                    dealt, new_logs = target.receive_damage(damage)
                    logs.extend(new_logs)
                    break

        elif self.tier == "Chunin":
            # Tấn công 2 kẻ địch đầu tiên còn sống
            targets = alive_enemies[:2]
            for target in targets:
                dealt, new_logs = target.receive_damage(damage)
                logs.extend(new_logs)

        elif self.tier == "Jounin":
            # Tấn công toàn bộ kẻ địch còn sống
            for target in alive_enemies:
                dealt, new_logs = target.receive_damage(damage)
                logs.extend(new_logs)

        elif self.tier == "Kage":
            # Sát thương chuẩn: bỏ qua giáp
            for target in alive_enemies:
                dealt, new_logs = target.receive_damage(damage, true_damage=True)
                logs.extend(new_logs)

        elif self.tier == "Legendary":
            for target in alive_enemies:
                # Gây sát thương chuẩn
                dealt, new_logs = target.receive_damage(damage, true_damage=True)
                logs.extend(new_logs)
                
                # Giảm giáp 30%
                armor_logs = target.reduce_armor_direct(percent_reduce=0.3)
                logs.extend(armor_logs)

        else:
            logs.append(f"{self.name} không có kỹ năng đặc biệt phù hợp.")

        return logs
