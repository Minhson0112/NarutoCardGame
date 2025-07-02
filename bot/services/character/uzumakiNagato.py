from bot.services.cardBase import Card

class UzumakiNagato(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌊 {self.name} sử dụng Ngoại Đạo Luân Hồi Chi Thuật, hồi sinh hoặc chữa lành đồng minh!")

        # 1️⃣ Tìm đồng minh đã chết
        dead_allies = [c for c in self.team if not c.is_alive()]
        if dead_allies:
            # Hồi sinh đồng minh đầu tiên với 100% HP
            target = dead_allies[0]
            target.health = target.max_health
            logs.append(f"💀 {target.name} được hồi sinh với {target.health}/{target.max_health} HP!")

            # Giảm tất cả chỉ số vĩnh viễn còn 50%
            orig_bd = target.base_damage
            target.base_damage = max(1, int(target.base_damage * 0.5))
            orig_armor = target.armor
            target.armor = int(target.armor * 0.5)
            orig_crit = target.crit_rate
            target.crit_rate = target.crit_rate * 0.5
            orig_speed = target.speed
            target.speed = target.speed * 0.5
            orig_chakra = target.chakra
            target.chakra = int(target.chakra * 0.5)

            logs.append(f"⚔️ {target.name} sát thương cơ bản: {orig_bd} → {target.base_damage}")
            logs.append(f"🛡️ {target.name} giáp: {orig_armor} → {target.armor}")
            logs.append(f"💥 {target.name} chí mạng: {orig_crit:.0%} → {target.crit_rate:.0%}")
            logs.append(f"🏃 {target.name} tốc độ: {orig_speed:.0%} → {target.speed:.0%}")
            logs.append(f"🔋 {target.name} chakra: {orig_chakra} → {target.chakra}")
        else:
            # 2️⃣ Nếu không có ai chết, hồi máu cho đồng minh thấp máu nhất bằng 400% SMKK
            heal_amount = int(self.get_effective_base_damage() * 4)
            alive = [c for c in self.team if c.is_alive()]
            if not alive:
                logs.append("❌ Không có đồng minh để hồi máu.")
            else:
                target = min(alive, key=lambda c: c.health / c.max_health)
                logs.append(f"💚 Không có đồng minh chết, hồi máu cho {target.name} (thấp máu nhất).")
                logs.extend(target.receive_healing(amount=heal_amount))

        return logs
