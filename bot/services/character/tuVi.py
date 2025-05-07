from bot.services.cardBase import Card
from bot.services.effect.sealChakraEffect import SealChakraEffect

class TuVi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🗡️ {self.name} 💣kích hoạt kỹ năng Bom vĩ thú! 💥 tấn công toàn bộ kẻ địch và phong ấn charka của chúng trong 3 turn")
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

            seal = SealChakraEffect(
                duration=3,
                description="Phong ấn chakra bởi Kushina"
            )
            target.effects.append(seal)
            logs.append(f"🔒 {target.name} bị phong ấn chakra trong 3 lượt và không thể nhận chakra!")

        return logs