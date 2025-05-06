from bot.services.cardBase import Card

class Konan(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🗡️ {self.name} tung Chiến Thuật Giấy, tấn công hai thành viên tuyến sau địch!")

        # Tính 800% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 8)
        # Lấy hai thành viên tuyến sau (chỉ số 1 và 2)
        backline = self.enemyTeam[1:3]
        targets = [c for c in backline if c.is_alive()]

        # Nếu không có thành viên tuyến sau nào còn sống, fallback tấn công tuyến đầu
        if not targets:
            logs.append("⚠️ Không tìm thấy tuyến sau còn sống, tấn công tuyến đầu thay thế!")
            first = next((c for c in self.enemyTeam if c.is_alive()), None)
            if first:
                targets = [first]

        if not targets:
            logs.append("❌ Không có mục tiêu nào để tấn công.")
            return logs

        for tgt in targets:
            dealt, new_logs = tgt.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(new_logs)

        return logs
