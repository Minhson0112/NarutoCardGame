from bot.services.cardBase import Card
from bot.services.effect.burnEffect import BurnEffect

class Kankuro(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("🎭 Kankuro điều khiển rối tung chiêu, tấn công toàn bộ kẻ địch và gây Độc!")
        damage = int(self.get_effective_base_damage())
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        for target in alive_enemies:
            # Gây sát thương cơ bản
            dealt, new_logs = target.receive_damage(damage, true_damage=False, execute_threshold=None, attacker=self)
            logs.extend(new_logs)

            # Kiểm tra hiệu ứng Burn đã tồn tại chưa
            exist_burn = next((e for e in target.effects if e.name == "Burn"), None)
            poison_damage =  damage # 100% sát thương cơ bản

            if exist_burn:
                # Cộng dồn damage và thời gian
                exist_burn.value += poison_damage
                exist_burn.duration += 1
                logs.append(
                    f"☠️ {target.name} bị cộng dồn hiệu ứng Độc: +{poison_damage} sát thương và +1 lượt."
                )
            else:
                # Tạo mới hiệu ứng Độc
                poison_effect = BurnEffect(
                    duration=1,
                    value=poison_damage,
                    description="Độc"
                )
                target.effects.append(poison_effect)
                logs.append(
                    f"☠️ {target.name} bị trúng Độc: {poison_damage} sát thương mỗi lượt trong 1 lượt."
                )

        return logs
