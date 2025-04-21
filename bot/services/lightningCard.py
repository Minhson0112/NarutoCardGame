from bot.services.cardBase import Card

class LightningCard(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"{self.name} kích hoạt kỹ năng đặc biệt hệ Lôi! ⚡")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        alive_allies = [c for c in self.team if c.is_alive()]

        damage = int(self.base_damage * 4)

        # Mặc định tăng né bản thân (riêng Legendary sẽ tăng cho toàn đội)
        def boost_speed(targets, boost_amount):
            for t in targets:
                original_speed = t.speed
                # cộng thêm nhưng không vượt quá 0.7
                t.speed = min(t.speed + boost_amount, 0.7)
                logs.append(
                    f"⚡ {t.name} được tăng né tránh từ {original_speed:.2f} "
                    f"lên {t.speed:.2f} (giới hạn 70%)"
                )

        if self.tier == "Genin":
            # Gây damage *4 lên tuyến đầu tiên còn sống
            for i in range(3):
                if self.enemyTeam[i].is_alive():
                    target = self.enemyTeam[i]
                    dealt = max(damage - target.armor, 0)
                    target.health -= dealt
                    if target.health < 0:
                        target.health = 0
                    logs.append(f"⚡ {target.name} nhận {dealt} sát thương mạnh từ sấm sét!")
                    break
            boost_speed([self], 0.05)

        elif self.tier == "Chunin":
            for i in range(3):
                if self.enemyTeam[i].is_alive():
                    target = self.enemyTeam[i]
                    dealt = max(damage - target.armor, 0)
                    target.health -= dealt
                    if target.health < 0:
                        target.health = 0
                    logs.append(f"⚡ {target.name} nhận {dealt} sát thương mạnh từ sấm sét!")
                    break
            boost_speed([self], 0.10)

        elif self.tier == "Jounin":
            targets = alive_enemies[:2]
            for target in targets:
                dealt = max(damage - target.armor, 0)
                target.health -= dealt
                if target.health < 0:
                    target.health = 0
                logs.append(f"⚡ {target.name} bị trúng đòn sét mạnh, mất {dealt} máu!")
            boost_speed([self], 0.15)

        elif self.tier == "Kage":
            for target in alive_enemies:
                dealt = max(damage - target.armor, 0)
                target.health -= dealt
                if target.health < 0:
                    target.health = 0
                logs.append(f"⚡ {target.name} bị giật sét toàn đội! Mất {dealt} máu.")
            boost_speed([self], 0.20)

        elif self.tier == "Legendary":
            for target in alive_enemies:
                dealt = max(damage - target.armor, 0)
                target.health -= dealt
                if target.health < 0:
                    target.health = 0
                logs.append(f"🌩️ {target.name} bị sét quét toàn đội! Mất {dealt} máu.")
            boost_speed(alive_allies, 0.20)

        else:
            logs.append(f"{self.name} không có kỹ năng đặc biệt phù hợp.")

        return logs
