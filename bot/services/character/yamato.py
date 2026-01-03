from bot.services.cardBase import Card
from bot.services.effect.rootEffect import RootEffect

class Yamato(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("🌳 Yamato thi triển Mộc Độn, trói chân và tấn công kẻ địch!")

        # 300% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 3)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        # Gây sát thương lên tất cả kẻ địch
        for target in alive_enemies:
            dealt, new_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(new_logs)

        # Trói chân tuyến đầu địch trong 2 turn
        front = next((c for c in alive_enemies if c.is_alive()), None)
        if front:
            root_effect = RootEffect(
                duration=2,
                description="Mộc Độn của Yamato"
            )
            blocked = False
            for p in target.passives:
                if p.name == "unEffect":
                    logs.extend(p.apply(target))
                    blocked = True
                    break
            if not blocked:
                front.effects.append(root_effect)
                logs.append(f"🌿 {front.name} bị trói chân 2 lượt, không thể dùng kỹ năng!")

        return logs
