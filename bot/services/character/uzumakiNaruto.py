from bot.services.cardBase import Card

class UzumakiNaruto(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(
            "💥 Rasensuriken kết hợp Bom Vĩ Thú! Một vụ nổ cực lớn san phẳng toàn bộ kẻ địch!"
        )

        # 600% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 4)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

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
