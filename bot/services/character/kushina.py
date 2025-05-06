from bot.services.cardBase import Card
from bot.services.effect.sealChakraEffect import SealChakraEffect

class Kushina(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("🔒🌸 Kushina thi triển thuật Phong Ấn Cực Mạnh, phong ấn chakra và tấn công toàn đội địch!")

        # 300% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 3)
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

            # 2️⃣ Phong ấn chakra 2 lượt
            seal = SealChakraEffect(
                duration=2,
                description="Phong ấn chakra bởi Kushina"
            )
            target.effects.append(seal)
            logs.append(f"🔒 {target.name} bị phong ấn chakra trong 2 lượt và không thể nhận chakra!")

        return logs
