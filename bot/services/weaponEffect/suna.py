
from bot.services.effectBase import Effect
from bot.services.effect.buffArmorEffect import BuffArmorEffect

class Suna(Effect):
    def __init__(self):
        super().__init__(
            name="armorProtection",
            duration=None,
            effect_type="condition",
            value=None,
            flat_bonus=0,
            description="nếu chịu sát thương và máu xuống dưới 20%, cho 1 lớp giáp 600 giáp trong 3 turn"
        )

    def apply(self, card, target = None):
        logs = []
        armor_buff = BuffArmorEffect(
            duration=3,
            value=0.0,
            flat_bonus=600,
            description=f"Giáp từ bảo hiểm của vũ khí Suna"
        )
        card.effects.append(armor_buff)
        logs.append(f"🛡️  {card.name} nhận 600 giáp trong 3 turn từ vũ khí Suna.")
        card.passives.remove(self)
        return logs

