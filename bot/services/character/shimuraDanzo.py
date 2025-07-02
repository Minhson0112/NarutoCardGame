from bot.services.cardBase import Card
from bot.services.effect.rootEffect import RootEffect

class ShimuraDanzo(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🗡️ {self.name} sử dụng Saringan, câm lặng và tấn công toàn bộ kẻ địch!")

        # 300% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 3)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

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

            # Áp dụng SilenceEffect 2 lượt
            silence = RootEffect(
                duration=2,
                description="Câm lặng từ Saringan của Danzo"
            )
            blocked = False
            for p in target.passives:
                if p.name == "unEffect":
                    logs.extend(p.apply(target))
                    blocked = True
                    break
            if not blocked:
                target.effects.append(silence)
                logs.append(f"🔇 {target.name} bị câm lặng 2 lượt, không thể dùng kỹ năng!")

        return logs
