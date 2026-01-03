from bot.services.cardBase import Card
from bot.services.effect.buffArmorEffect import BuffArmorEffect

class HyugaNeji(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🛡️ Hyuga Neji kích hoạt Bát Quái Bảo Kính, tăng phòng thủ và hồi máu!")

        neji_damage = self.get_effective_base_damage()
        # Tăng giáp: 100% SMKK trong 3 turn
        armor_buff = BuffArmorEffect(
            duration=3,
            value=0,  # Không buff theo %
            flat_bonus=neji_damage,
            description=f"Tăng giáp của Neji (+{neji_damage})"
        )
        self.effects.append(armor_buff)
        logs.append(f"🛡️ {self.name} tăng {neji_damage} giáp trong 3 lượt.")

        # Hồi 20% máu đã mất
        missing_hp = self.max_health - self.health
        healing = int(missing_hp * 0.2)
        if healing > 0:
            heal_logs = self.receive_healing(amount=healing)
            logs.extend(heal_logs)
        else:
            logs.append(f"{self.name} không mất máu nên không cần hồi phục.")

        return logs
