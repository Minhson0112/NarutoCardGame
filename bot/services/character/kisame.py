from bot.services.cardBase import Card
from bot.services.effect.buffArmorEffect import BuffArmorEffect
from bot.services.effect.stunEffect import StunEffect

class Kisame(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"💧 {self.name} sử dụng Thủy Ngục, giam cầm tuyến đầu địch và gia tăng giáp bản thân!")

        # 1️⃣ Trói chân tuyến đầu địch (stun) trong 3 lượt
        front = next((c for c in self.enemyTeam if c.is_alive()), None)
        if front:
            stun = StunEffect(
                duration=3,
                description="Thủy Ngục của Kisame"
            )
            
            blocked = False
            for p in front.passives:
                if p.name == "unStun":
                    logs.extend(p.apply(front))
                    blocked = True
                    break
            if not blocked:
                front.effects.append(stun)
                logs.append(f"⚡ {front.name} bị giam trong thuỷ ngục và bị mất 3 lượt!")
        else:
            logs.append("❌ Không tìm thấy mục tiêu tuyến đầu để trói chân.")

        # 2️⃣ Tăng giáp bản thân bằng 200% SMKK trong 5 lượt
        flat_bonus = int(self.get_effective_base_damage() * 2)
        armor_buff = BuffArmorEffect(
            duration=5,
            value=0,  # không dùng % giáp hiện tại
            flat_bonus=flat_bonus,
            description="Giáp Thủy Ngục của Kisame"
        )
        self.effects.append(armor_buff)
        logs.append(f"🛡️ {self.name} nhận buff +{flat_bonus} giáp trong 2 lượt (200% SMKK).")

        return logs
