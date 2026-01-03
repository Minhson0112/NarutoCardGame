from bot.services.cardBase import Card
from bot.services.effectBase import Effect

class HokageKakashi(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌀 {self.name}  Ninja Sao Chép: sao chép mọi hiệu ứng buff của đối thủ và tấn công toàn diện!")

        # Sao chép tất cả hiệu ứng buff từ team địch
        for enemy in self.enemyTeam:
            for effect in enemy.effects:
                if effect.effect_type == "buff":
                    # Tạo bản sao của effect
                    copied = Effect(
                        name=effect.name,
                        duration=effect.duration,
                        effect_type=effect.effect_type,
                        value=effect.value,
                        flat_bonus=effect.flat_bonus,
                        description=f"Sao chép {effect.description} từ {enemy.name}"
                    )
                    self.effects.append(copied)
                    logs.append(f"🔄 Sao chép {effect.description} từ {enemy.name} trong {effect.duration} lượt).")

        # Tấn công toàn bộ kẻ địch với 400% sát thương cơ bản
        damage = int(self.get_effective_base_damage() * 4)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        for target in alive_enemies:
            dealt, new_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(new_logs)

        return logs
