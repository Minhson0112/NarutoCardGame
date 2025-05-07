from bot.services.cardBase import Card
from bot.services.effect.buffArmorEffect import BuffArmorEffect

class BatVi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🗡️ {self.name} 💣kích hoạt kỹ năng Bom vĩ thú! 💥 tấn công toàn bộ kẻ địch và tăng giáp bằng 100% smkk trong 4 turn")
        # Lấy tất cả kẻ địch còn sống
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.get_effective_base_damage() * 3)
        flat_bonus = self.get_effective_base_damage()
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

        armor_buff = BuffArmorEffect(
            duration=4,
            value=0.0,                # không dùng % cơ bản
            flat_bonus=flat_bonus,
            description=f"hiệu ứng Giáp của {self.name}"
        )
        self.effects.append(armor_buff)
        logs.append(
            f"🛡️ {self.name} nhận buff +{flat_bonus} giáp "
            f"(100% SMKK của {self.name}) trong 4 lượt!"
        )

        return logs