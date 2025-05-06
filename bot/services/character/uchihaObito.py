from bot.services.cardBase import Card
from bot.services.effect.buffDamageEffect import BuffDamageEffect
from bot.services.effect.buffCritEffect import BuffCritEffect

class UchihaObito(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌑 {self.name} Tộc nhân Uchiha, tăng chí mạng và sức mạnh tấn công!")

        # 1️⃣ Tăng chí mạng lên 100% trong 6 lượt
        crit_buff = BuffCritEffect(
            duration=6,
            value=1.0,  # +100% crit rate
            description="Chí mạng của Obito"
        )
        self.effects.append(crit_buff)
        logs.append(f"💥 {self.name} tăng tỉ lệ chí mạng lên 100% trong 6 lượt!")

        # 2️⃣ Tăng sát thương cơ bản lên 200% (tức gấp đôi) trong 6 lượt
        dmg_buff = BuffDamageEffect(
            duration=6,
            value=1.0,  # +100% tức gấp đôi sát thương cơ bản
            description="Sức mạnh tấn công của Obito"
        )
        self.effects.append(dmg_buff)
        logs.append(f"⚔️ {self.name} tăng sát thương cơ bản lên 200% trong 6 lượt!")

        return logs
