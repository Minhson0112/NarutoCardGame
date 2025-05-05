from bot.services.effectBase import Effect

class IllusionEffect(Effect):
    def __init__(self, duration, description="Ảo Thuật: hoán đổi team và enemyTeam"):
        super().__init__(
            name="Illusion",
            duration=duration,
            effect_type="debuff",
            value=None,
            description=description
        )
        # Lưu team gốc để khôi phục khi hết hiệu lực
        self.original_team = None
        self.original_enemy_team = None
        self.trigger_on_pre_action = True
        self.is_swapped = False  #  Thêm flag

    def apply(self, card):
        logs = []

        # Chỉ swap nếu chưa từng swap lần nào
        if not self.is_swapped:
            # Lưu lại trạng thái ban đầu
            self.original_team = card.team
            self.original_enemy_team = card.enemyTeam

            # Hoán đổi team
            card.team, card.enemyTeam = card.enemyTeam, card.team

            self.is_swapped = True  #  Đánh dấu đã swap

            logs.append(f"🎭 {card.name} bị trúng Ảo Thuật và tạm thời coi đồng minh là địch, địch là đồng minh!")

        return logs

    def on_expire(self, card):
        logs = []

        # Reset về trạng thái ban đầu nếu đã từng swap
        if self.is_swapped:
            card.team = self.original_team
            card.enemyTeam = self.original_enemy_team
            logs.append(f"🌀 Ảo Thuật trên {card.name} đã hết hiệu lực, trở lại bình thường.")

        return logs
