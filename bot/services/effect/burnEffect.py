from bot.services.effectBase import Effect

class BurnEffect(Effect):
    def __init__(self, duration, value, description="Burn"):
        super().__init__(name="Burn", duration=duration, effect_type="debuff", value=value, description=description)

    def apply(self, card):
        damage = self.value
        card.health -= damage
        if card.health < 0:
            card.health = 0
        return [f"🔥 {card.name} chịu {damage} sát thương từ {self.description}."]