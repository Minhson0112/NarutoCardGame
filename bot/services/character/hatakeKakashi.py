from bot.services.cardBase import Card
from bot.services.effect.deBuffArmorEffect import DebuffArmorEffect

class HatakeKakashi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"⚡️ {self.name} sử dụng Chidori Cực Mạnh: càn quét toàn bộ kẻ địch với sát thương chuẩn!")

        # Tính 800% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 5)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            # 1️⃣ Gây sát thương chuẩn (bỏ qua giáp)
            dealt, dmg_logs = target.receive_damage(
                damage,
                true_damage=True,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(dmg_logs)

            # 2️⃣ Phá giáp 80% trong 2 lượt
            armor_debuff = DebuffArmorEffect(
                duration=2,
                value=0.8,  # giảm 80% giáp
                description=f"Phá giáp từ Chidori của {self.name}"
            )
            target.effects.append(armor_debuff)
            logs.append(f"🛡️ {target.name} bị giảm 80% giáp trong 2 lượt!")

        return logs
