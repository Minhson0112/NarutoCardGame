from bot.services.cardBase import Card
from bot.services.effect.stunEffect import StunEffect

class Konohamaru(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("💫 Konohamaru sử dụng Thuật Quyến Rũ khiến toàn bộ kẻ địch mê hoặc!")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        stun_duration = 1  # Choáng 1 lượt

        for target in alive_enemies:

            stun_effect = StunEffect(
                duration=stun_duration,
                description="Mê hoặc của Konohamaru"
            )
            blocked = False
            for p in target.passives:
                if p.name == "unStun":
                    logs.extend(p.apply(target))
                    blocked = True
                    break
            if not blocked:
                target.effects.append(stun_effect)
                logs.append(f"⚡ {target.name} bị choáng {stun_duration} lượt.")

        return logs