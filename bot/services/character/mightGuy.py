from bot.services.cardBase import Card

class MightGuy(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🔥 {self.name} mở Bát Môn, hi sinh một phần để đạt sức mạnh vượt trội!")

        # 1️⃣ Hi sinh 10% máu hiện tại
        sacrifice = int(self.health * 0.1)
        self.health = max(0, self.health - sacrifice)
        logs.append(f"💔 {self.name} hi sinh {sacrifice} HP để kích hoạt Bát Môn!")

        # 2️⃣ Buff vĩnh viễn: tăng toàn bộ chỉ số lên 250% (tức x2.5, thêm 1.5 lần giá trị hiện tại)
        # Tính phần cần buff thêm để đạt 2.5× so với hiện tại
        base_increase  = int(self.base_damage * 1.5)
        armor_increase = int(self.armor      * 1.5)
        crit_increase  = self.crit_rate      * 1.5
        speed_increase = self.speed          * 1.5
        chakra_increase = int(self.chakra     * 1.5)

        # Áp dụng buff trực tiếp
        logs.extend(self.receive_base_damage_buff(base_increase))
        logs.extend(self.receive_armor_buff(armor_increase))
        logs.extend(self.receive_crit_buff(crit_increase))
        logs.extend(self.receive_speed_buff(speed_increase))
        logs.extend(self.receive_chakra_buff(chakra_increase))

        return logs
