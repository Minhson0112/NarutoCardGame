from bot.services.cardBase import Card

class AburameShino(Card):
    def special_skills(self):
        logs: list[str] = []

        logs.append("🐛 Shino điều khiển bọ ký sinh hút chakra đối phương và truyền cho đồng minh!")

        # 1️⃣ Tìm đối phương tuyến đầu còn sống
        target = None
        for c in self.enemyTeam:
            if c.is_alive():
                target = c
                break

        if not target:
            logs.append("❌ Không tìm thấy mục tiêu tuyến đầu để hút chakra.")
            return logs

        # 2️⃣ Hút chakra = 50% sát thương cơ bản
        suck_amount = int(self.get_effective_base_damage() * 0.5)
        if target.chakra <= 0:
            logs.append(f"⚠️ {target.name} không có chakra để hút.")
            actual_drained = 0
        else:
            actual_drained = min(suck_amount, target.chakra)
            drain_logs = target.reduce_chakra_direct(actual_drained)
            logs.extend(drain_logs)

        if actual_drained == 0:
            logs.append("⚠️ Không có chakra nào được truyền cho đồng minh.")
            return logs

        # 3️⃣ Tìm đồng minh nhiều chakra nhất để buff
        allies_alive = [c for c in self.team if c.is_alive()]
        if not allies_alive:
            logs.append("❌ Không tìm thấy đồng minh để buff chakra.")
            return logs

        # Tìm đồng minh có chakra cao nhất
        max_chakra_ally = max(allies_alive, key=lambda c: c.chakra)
        buff_logs = max_chakra_ally.receive_chakra_buff(actual_drained)
        logs.extend(buff_logs)

        return logs