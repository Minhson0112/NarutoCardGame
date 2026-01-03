from bot.services.cardBase import Card
from bot.services.effect.buffSpeedEffect import BuffSpeedEffect

class Minato(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"⚡️ {self.name} sử dụng Phi Tiêu Thần Tốc: tăng né tránh và tấn công toàn diện!")

        # Tăng né tránh lên 70% trong 3 lượt
        speed_buff = BuffSpeedEffect(
            duration=3,
            value=0.7,  # +70% speed, sẽ được clamp bởi get_effective_speed()
            flat_bonus=0,
            description=f"Tốc độ Chạng Vạng của {self.name}"
        )
        self.effects.append(speed_buff)
        logs.append(f"🏃 {self.name} tăng né tránh lên 70% trong 3 lượt!")

        # Gây 500% sát thương cơ bản lên toàn bộ kẻ địch
        damage = int(self.get_effective_base_damage() * 5)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào còn sống để tấn công.")
            return logs

        for target in alive_enemies:
            dealt, new_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=0.2,  # Kết liễu nếu xuống dưới 20% HP tối đa
                attacker=self
            )
            logs.extend(new_logs)

        return logs
