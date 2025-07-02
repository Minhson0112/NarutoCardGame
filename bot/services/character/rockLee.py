from bot.services.cardBase import Card

class RockLee(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🔥 {self.name} mở Ngũ Môn, hi sinh máu để nhân đôi toàn bộ chỉ số!")

        # 1️⃣ Tiêu tốn 20% máu hiện tại
        sacrifice = int(self.health * 0.2)
        self.health -= sacrifice
        if self.health < 0:
            self.health = 0
        logs.append(f"💔 {self.name} tự giảm {sacrifice} HP để kích hoạt Ngũ Môn!")

        # 2️⃣ Buff: nhân đôi tất cả chỉ số (có cộng dồn)
        # Tính phần cần buff thêm để đạt x2 (vd: buff thêm đúng base_damage hiện tại)
        base_buff = min(self.base_damage, 3500)
        armor_buff = min(self.armor, 600)
        crit_buff = self.crit_rate
        speed_buff = self.speed

        # Tăng sát thương cơ bản
        logs.extend(self.receive_base_damage_buff(base_buff))
        # Tăng giáp
        logs.extend(self.receive_armor_buff(armor_buff))
        # Tăng chí mạng
        logs.extend(self.receive_crit_buff(crit_buff))
        # Tăng né tránh
        logs.extend(self.receive_speed_buff(speed_buff))

        return logs
