from bot.services.cardBase import Card
from bot.services.effect.immuneEffect import ImmuneEffect

class SenjuTobirama(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"⚔️ {self.name} sử dụng Cấm Thuật: càn quét kẻ địch và tự bảo hộ!")

        # 1️⃣ Gây 400% sát thương cơ bản lên toàn bộ kẻ địch
        damage = int(self.get_effective_base_damage() * 4)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]
        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
        else:
            for target in alive_enemies:
                dealt, dmg_logs = target.receive_damage(
                    damage,
                    true_damage=False,
                    execute_threshold=None,
                    attacker=self
                )
                logs.extend(dmg_logs)

        # 2️⃣ Giải trừ mọi hiệu ứng bất lợi trên bản thân
        removed = [e for e in self.effects if e.effect_type == 'debuff']
        self.effects = [e for e in self.effects if e.effect_type != 'debuff']
        for e in removed:
            logs.append(f"❎ Hiệu ứng '{e.description}' trên {self.name} đã bị giải trừ.")

        # 3️⃣ Phong ấn miễn nhiễm sát thương trong 3 lượt
        immune = ImmuneEffect(duration=3, description="Miễn nhiễm sát thương từ Cấm Thuật của Tobirama")
        self.effects.append(immune)
        logs.append(f"🛡️ {self.name} được miễn nhiễm sát thương trong 3 lượt tới!")

        return logs
