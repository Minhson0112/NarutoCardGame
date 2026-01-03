from bot.services.cardBase import Card
from bot.services.effect.deBuffArmorEffect import DebuffArmorEffect
from bot.services.effect.deBuffCritEffect import DebuffCritEffect
from bot.services.effect.deBuffDamageEffect import DebuffDamageEffect
from bot.services.effect.deBuffSpeedEffect import DebuffSpeedEffect

class Onoki(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🪨 {self.name} tung Trần Độn, càn quét toàn bộ kẻ địch và suy yếu!")

        # Gây 200% sát thương cơ bản lên tất cả kẻ địch
        damage = int(self.get_effective_base_damage() * 2)
        alive_enemies = [c for c in self.enemyTeam if c.is_alive()]

        if not alive_enemies:
            logs.append("❌ Không có kẻ địch nào để tấn công.")
            return logs

        # Áp dụng sát thương và giảm 50% toàn bộ chỉ số trong 2 lượt
        duration = 2
        for target in alive_enemies:
            dealt, dmg_logs = target.receive_damage(
                damage,
                true_damage=False,
                execute_threshold=None,
                attacker=self
            )
            logs.extend(dmg_logs)

            # Giảm giáp
            armor_debuff = DebuffArmorEffect(
                duration=duration,
                value=0.5,
                description="Giảm giáp từ Trần Độn của Onoki"
            )
            target.effects.append(armor_debuff)
            logs.append(f"🛡️ {target.name} bị giảm 50% giáp trong {duration} lượt!")

            # Giảm chí mạng
            crit_debuff = DebuffCritEffect(
                duration=duration,
                value=0.5,
                description="Giảm chí mạng từ Trần Độn của Onoki"
            )
            target.effects.append(crit_debuff)
            logs.append(f"💥 {target.name} bị giảm 50% chí mạng trong {duration} lượt!")

            # Giảm sát thương cơ bản
            damage_debuff = DebuffDamageEffect(
                duration=duration,
                value=0.5,
                description="Giảm sát thương từ Trần Độn của Onoki"
            )
            target.effects.append(damage_debuff)
            logs.append(f"⚔️ {target.name} bị giảm 50% sát thương trong {duration} lượt!")

            # Giảm tốc độ
            speed_debuff = DebuffSpeedEffect(
                duration=duration,
                value=0.5,
                description="Giảm tốc độ từ Trần Độn của Onoki"
            )
            target.effects.append(speed_debuff)
            logs.append(f"🏃 {target.name} bị giảm 50% tốc độ trong {duration} lượt!")

        return logs
