from bot.services.cardBase import Card
from bot.services.effect.stunEffect import StunEffect

class UchihaMadara(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("💥 Madara dùng Susano đập mạnh gây sát thương chuẩn và làm choáng cả team địch trong 2 turn!")
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.get_effective_base_damage() * 6)

        for target in alive_enemies:
            new_stun_duration = 2
            exist_stun = next((e for e in target.effects if e.name == "Stun"), None)

            if exist_stun:
                if new_stun_duration > exist_stun.duration:
                    exist_stun.duration = new_stun_duration
                    logs.append(f"⚡ {target.name} bị làm mới thời gian choáng ({new_stun_duration} lượt).")
                else:
                    logs.append(f"⚡ {target.name} đã bị dính hiệu ứng choáng lâu hơn, không thay đổi.")
            else:
                stun_effect = StunEffect(
                    duration=new_stun_duration,
                    description="Choáng của Madara"
                )
                target.effects.append(stun_effect)
                logs.append(f"⚡ {target.name} bị choáng {new_stun_duration} lượt.")

            # Gây sát thương chuẩn
            dealt, new_logs = target.receive_damage(damage, true_damage=True, execute_threshold=None, attacker=self)
            logs.extend(new_logs)

        return logs