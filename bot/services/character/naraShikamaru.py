from bot.services.cardBase import Card
from bot.services.effect.stunEffect import StunEffect

class NaraShikamaru(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌀 {self.name} sử dụng Thuật Trói Bóng, trói toàn bộ kẻ địch và tự hạn chế bản thân!")

        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        stun_duration = 2

        # Trói toàn bộ kẻ địch
        for target in alive_enemies:
            exist_stun = next((e for e in target.effects if e.name == "Stun"), None)
            if exist_stun:
                if stun_duration > exist_stun.duration:
                    exist_stun.duration = stun_duration
                    logs.append(f"⚡ {target.name} bị làm mới thời gian choáng ({stun_duration} lượt).")
                else:
                    logs.append(f"⚡ {target.name} đã bị dính choáng lâu hơn, không thay đổi.")
            else:
                stun_effect = StunEffect(
                    duration=stun_duration,
                    description="Trói bóng của Shikamaru"
                )
                target.effects.append(stun_effect)
                logs.append(f"⚡ {target.name} bị trói bóng {stun_duration} lượt.")

        # Trói chính bản thân Shikamaru
        self_stun = StunEffect(
            duration=stun_duration,
            description="Tự hạn chế do Trói Bóng"
        )
        self.effects.append(self_stun)
        logs.append(f"⚠️ {self.name} cũng tự trói bản thân trong {stun_duration} lượt.")

        return logs
