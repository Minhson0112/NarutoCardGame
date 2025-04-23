from bot.services.cardBase import Card

class TailedBeastCard(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"{self.name} kích hoạt kỹ năng Bom vĩ thú! 💥")

        # Lấy danh sách kẻ địch còn sống
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        damage = int(self.base_damage * 2)

        # Xác định phần trăm giảm giáp theo tier (1vi -> 5%, 2vi -> 10%, ...)
        try:
            count = int(self.tier.replace("vi", ""))
            armor_reduction_percent = count * 0.05
        except Exception:
            armor_reduction_percent = 0.0

        # Áp dụng sát thương và giảm giáp cho tất cả kẻ địch
        for target in alive_enemies:
            # Tính sát thương có xét giáp
            dealt = max(damage - target.armor, 0)
            target.health -= dealt
            if target.health < 0:
                target.health = 0
            logs.append(
                f"💥 {target.name} nhận {dealt} sát thương từ bom vĩ thú!"
            )

            # Giảm giáp theo phần trăm
            reduction_amount = int(target.armor * armor_reduction_percent)
            target.armor = max(target.armor - reduction_amount, 0)
            logs.append(
                f"🛡️ Giảm giáp của {target.name} đi {int(armor_reduction_percent*100)}% ({reduction_amount})."
            )

        return logs
