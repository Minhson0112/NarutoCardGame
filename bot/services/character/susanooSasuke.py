from bot.services.cardBase import Card
from bot.services.effect.stunEffect import StunEffect

class SusanooSasuke(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🎯 {self.name} triệu hồi Susano'o và bắn cung tên cực mạnh!")

        # 600% sát thương cơ bản (tức nhân 10 lần)
        damage = int(self.get_effective_base_damage() * 8)
        # Xác định mục tiêu tuyến đầu còn sống
        target = next((c for c in self.enemyTeam if c.is_alive()), None)
        if not target:
            logs.append("❌ Không tìm thấy mục tiêu để tấn công.")
            return logs

        # Gây sát thương thường
        dealt, dmg_logs = target.receive_damage(
            damage,
            true_damage=False,
            execute_threshold=None,
            attacker=self
        )
        logs.extend(dmg_logs)

        # Áp dụng choáng 1 lượt
        stun = StunEffect(
            duration=1,
            description=f"Choáng từ Susano'o của {self.name}"
        )
        blocked = False
        for p in target.passives:
            if p.name == "unStun":
                logs.extend(p.apply(target))
                blocked = True
                break
        if not blocked:
            target.effects.append(stun)
            logs.append(f"⚡ {target.name} bị choáng 1 lượt!")

        return logs
