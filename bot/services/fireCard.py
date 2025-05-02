from bot.services.cardBase import Card
from bot.services.effect import Effect
class FireCard(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"{self.name} kích hoạt kỹ năng đặc biệt hệ Hỏa! 🔥")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.base_damage * 5)
        
        if self.name == "Uchiha Madara":
            for target in alive_enemies:
                # Thêm hiệu ứng stun 2 turn
                stun_effect = Effect(
                    name="Stun",
                    duration=2,
                    effect_type="debuff",
                    value=None,
                    description="Không thể hành động trong 2 lượt."
                )
                target.effects.append(stun_effect)
                # Gây sát thương chuẩn (bạn không nói rõ có qua giáp hay không, mặc định là thường)
                dealt, new_logs = target.receive_damage(damage, true_damage=True)
                logs.extend(new_logs)

            logs.append(
                f"💥 Madara dùng Susano đập mạnh gây sát thương chuẩn và làm choáng cả team địch trong 2 turn!"
            )
            return logs
        
        if self.tier == "Genin":
            # Tấn công hàng đầu tiên còn sống
            for i in range(3):
                if self.enemyTeam[i].is_alive():
                    target = self.enemyTeam[i]
                    target.health -= max(damage - target.armor, 0)
                    if target.health < 0:
                        target.health = 0
                    logs.append(f"🔥 {target.name} bị tấn công bằng hỏa thuật! Gây {max(damage - target.armor, 0)} sát thương.")
                    break

        elif self.tier == "Chunin":
            # Tấn công 2 kẻ địch đầu tiên còn sống
            targets = alive_enemies[:2]
            for target in targets:
                dealt = max(damage - target.armor, 0)
                target.health -= dealt
                if target.health < 0:
                    target.health = 0
                logs.append(f"🔥 {target.name} nhận {dealt} sát thương từ hỏa thuật!")

        elif self.tier == "Jounin":
            # Tấn công toàn bộ kẻ địch còn sống
            for target in alive_enemies:
                dealt = max(damage - target.armor, 0)
                target.health -= dealt
                if target.health < 0:
                    target.health = 0
                logs.append(f"🔥 {target.name} bị thiêu đốt! Gây {dealt} sát thương.")

        elif self.tier == "Kage":
            # Sát thương chuẩn: bỏ qua giáp
            for target in alive_enemies:
                target.health -= damage
                if target.health < 0:
                    target.health = 0
                logs.append(f"🔥🔥 {target.name} nhận {damage} sát thương chuẩn (bỏ qua giáp)!")

        elif self.tier == "Legendary":
            # Sát thương chuẩn + giảm giáp 30%
            for target in alive_enemies:
                target.health -= damage
                armor_reduction = int(target.armor * 0.3)
                target.armor = max(target.armor - armor_reduction, 0)
                if target.health < 0:
                    target.health = 0
                logs.append(f"🌋 {target.name} bị hủy diệt! Gây {damage} sát thương chuẩn và giảm giáp {armor_reduction}!")

        else:
            logs.append(f"{self.name} không có kỹ năng đặc biệt phù hợp.")

        return logs
