from bot.services.cardBase import Card

class NoharaRin(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"💖 Nohara Rin kích hoạt thuật y thuật, hồi máu cho đồng đội!")

        healing_amount = int(self.get_effective_base_damage() * 5)

        # Lọc các đồng minh còn sống (trừ chính Rin nếu không tự hồi)
        alive_allies = [c for c in self.team if c.is_alive()]

        if not alive_allies:
            logs.append("❌ Không có đồng minh nào để hồi máu.")
            return logs

        # Sắp xếp theo % máu còn lại tăng dần
        sorted_allies = sorted(
            alive_allies,
            key=lambda c: c.health / c.max_health if c.max_health else 1
        )

        # Hồi cho 2 đồng minh thấp máu nhất
        for target in sorted_allies[:2]:
            heal_logs = target.receive_healing(amount=healing_amount)
            logs.extend(heal_logs)

        return logs
