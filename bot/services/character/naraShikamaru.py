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

            stun_effect = StunEffect(
                duration=stun_duration,
                description="Trói bóng của Shikamaru"
            )
            blocked = False
            for p in target.passives:
                if p.name == "unStun":
                    logs.extend(p.apply(target))
                    blocked = True
                    break
            if not blocked:
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
