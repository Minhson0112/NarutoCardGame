from bot.services.cardBase import Card
from bot.services.effect.immuneEffect import ImmuneEffect

class NguVi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🗡️ {self.name} 💣kích hoạt kỹ năng Bom vĩ thú! 💥 tấn công toàn bộ kẻ địch và cho bạn thân hiệu ứng miễn thương trong 3 turn")
        # Lấy tất cả kẻ địch còn sống
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.get_effective_base_damage() * 2)

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            # Gây sát thương
            dealt, dmg_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(dmg_logs)

        immune = ImmuneEffect(duration=3, description="Miễn nhiễm sát thương của Ngũ Vĩ")
        self.effects.append(immune)
        logs.append(f"🛡️ {self.name} được miễn nhiễm sát thương trong 3 lượt tới!")

        return logs