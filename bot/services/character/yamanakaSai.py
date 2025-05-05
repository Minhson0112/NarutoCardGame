from bot.services.cardBase import Card

class YamanakaSai(Card):
    def special_skills(self):
        logs: list[str] = []

        logs.append("🎨🐯 Sai vẽ hổ, hổ lập tức vồ lấy toàn bộ kẻ địch!")

        # 300% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 3)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để hổ vồ.")
            return logs

        for target in alive_enemies:
            # Gây sát thương thường và kết liễu nếu dưới 5% máu tối đa
            dealt, new_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=0.05,
                attacker=self
            )
            logs.extend(new_logs)

        return logs
