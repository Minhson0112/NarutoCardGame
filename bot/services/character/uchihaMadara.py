from bot.services.cardBase import Card
from bot.services.effect.stunEffect import StunEffect

class UchihaMadara(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("💥 Madara dùng Susano đập mạnh gây sát thương chuẩn và làm choáng cả team địch trong 2 turn!")
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.get_effective_base_damage() * 4)

        for target in alive_enemies:
            new_stun_duration = 2
            stun_effect = StunEffect(
                duration=new_stun_duration,
                description="Choáng của Madara"
            )
            blocked = False
            for p in target.passives:
                if p.name == "unStun":
                    logs.extend(p.apply(target))
                    blocked = True
                    break
            if not blocked:
                target.effects.append(stun_effect)
                logs.append(f"⚡ {target.name} bị choáng {new_stun_duration} lượt.")

            # Gây sát thương chuẩn
            dealt, new_logs = target.receive_damage(damage, true_damage=True, execute_threshold=None, attacker=self)
            logs.extend(new_logs)

        return logs