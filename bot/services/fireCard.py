from bot.services.cardBase import Card
from bot.services.effect import Effect
class FireCard(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"{self.name} kích hoạt kỹ năng đặc biệt hệ Hỏa! 🔥")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.get_effective_base_damage * 5)
        
        if self.name == "Uchiha Madara":
            for target in alive_enemies:
                new_stun_duration = 2
                exist_stun = next((e for e in target.effects if e.name == "Stun"), None)

                if exist_stun:
                    if new_stun_duration > exist_stun.duration:
                        exist_stun.duration = new_stun_duration
                        logs.append(f"⚡ {target.name} bị làm mới thời gian choáng ({new_stun_duration} lượt).")
                    else:
                        logs.append(f"⚡ {target.name} đã bị dính hiệu ứng choáng lâu hơn, không thay đổi.")
                else:
                    stun_effect = Effect(
                        name="Stun",
                        duration=new_stun_duration,
                        effect_type="debuff",
                        value=None,
                        description="Choáng của Madara"
                    )
                    target.effects.append(stun_effect)
                    logs.append(f"⚡ {target.name} bị choáng 2 lượt.")

                # Gây sát thương chuẩn
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
