from bot.services.cardBase import Card
from bot.services.effect.stunEffect import StunEffect

class Konohamaru(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("💫 Konohamaru sử dụng Thuật Quyến Rũ khiến toàn bộ kẻ địch mê hoặc!")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        stun_duration = 1  # Choáng 1 lượt

        for target in alive_enemies:
            exist_stun = next((e for e in target.effects if e.name == "Stun"), None)

            if exist_stun:
                if stun_duration > exist_stun.duration:
                    exist_stun.duration = stun_duration
                    logs.append(f"⚡ {target.name} bị làm mới thời gian choáng ({stun_duration} lượt).")
                else:
                    logs.append(f"⚡ {target.name} đã bị dính hiệu ứng khống chế lâu hơnhơn, không thay đổi.")
            else:
                stun_effect = StunEffect(
                    duration=stun_duration,
                    description="Mê hoặc của Konohamaru"
                )
                target.effects.append(stun_effect)
                logs.append(f"⚡ {target.name} bị choáng {stun_duration} lượt.")

        return logs