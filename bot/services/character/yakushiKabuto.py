from bot.services.cardBase import Card

class YakushiKabuto(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append("🌿 Yakushi Kabuto thi triển Uế Thổ Chuyển Sinh!")

        # Tìm đồng minh đã chết
        dead_allies = [c for c in self.team if not c.is_alive()]
        if dead_allies:
            # Hồi sinh đồng minh đầu tiên đã chết với 50% máu tối đa
            target = dead_allies[0]
            revive_hp = int(target.max_health * 0.5)
            target.health = revive_hp
            logs.append(
                f"💀 {target.name} được hồi sinh với {revive_hp}/{target.max_health} HP!"
            )
        else:
            # Nếu không có ai chết, hồi máu cho cả team bằng 200% SMKK
            heal_amount = int(self.get_effective_base_damage() * 2)
            logs.append(
                f"💚 Không có đồng minh nào chết, Kabuto hồi máu cho toàn đội (+{heal_amount} HP mỗi người)!"
            )
            for ally in self.team:
                if ally.is_alive():
                    logs.extend(ally.receive_healing(amount=heal_amount))

        return logs