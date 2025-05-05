from bot.services.cardBase import Card
from bot.services.effect.buffArmorEffect import BuffArmorEffect

class HarunoSakura(Card):
    def special_skills(self):
        logs: list[str] = []

        logs.append("🌸 Sakura vận dụng y thuật hồi phục và cường hóa giáp cho đồng đội!")

        #Tìm đồng minh thấp máu nhất (còn sống)
        allies_alive = [c for c in self.team if c.is_alive()]
        if not allies_alive:
            logs.append("❌ Không tìm thấy đồng minh nào để hồi phục.")
            return logs

        target = min(allies_alive, key=lambda c: c.health / c.max_health)

        #Hồi phục: 500% sát thương cơ bản
        heal_amount = int(self.get_effective_base_damage() * 5)
        heal_logs = target.receive_healing(amount=heal_amount)
        logs.extend(heal_logs)

        #Buff giáp: 50% sát thương cơ bản trong 3 lượt
        armor_value = 0.5  # +50% giáp (theo % giáp hiện tại)
        flat_bonus = int(self.get_effective_base_damage() * 0.5)  # Thêm bonus cố định nếu cần

        armor_buff = BuffArmorEffect(
            duration=3,
            value=armor_value,
            flat_bonus=flat_bonus,
            description="Tăng giáp từ Sakura"
        )
        target.effects.append(armor_buff)
        logs.append(f"🛡️ {target.name} nhận buff giáp +{flat_bonus} trong 3 lượt.")

        return logs
