from bot.services.cardBase import Card

class UzumakiNaruto(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(
            "💥 Rasensuriken kết hợp Bom Vĩ Thú! Một vụ nổ cực lớn san phẳng toàn bộ kẻ địch!"
        )

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        hp_ratio = self.health / self.max_health
        if hp_ratio < 0.3:
            damage = int(self.get_effective_base_damage() * 10)
            logs.append("⚠️ Naruto tiến hóa lên mode lục đạo! Rasensuriken bộc phát với sức mạnh hủy diệt 1000%!")
        else:
            damage = int(self.get_effective_base_damage() * 4)

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            # 1️⃣ Gây sát thương thường
            dealt, dmg_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(dmg_logs)

            # 2️⃣ Làm mất hết chakra của mục tiêu
            if target.chakra > 0:
                reduce_logs = target.reduce_chakra_direct(40)
                logs.extend(reduce_logs)
            else:
                logs.append(f"🔋 {target.name} đã hết chakra.")

        return logs
