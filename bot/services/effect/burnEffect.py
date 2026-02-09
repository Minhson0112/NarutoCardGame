from bot.services.i18n import t
from bot.services.effectBase import Effect

class BurnEffect(Effect):
    def __init__(self, duration, value, description=""):
        super().__init__(
            name="Burn",
            duration=duration,
            effect_type="debuff",
            value=value,
            description=description,
        )

    def apply(self, card):
        guild_id = getattr(card, "guild_id", None)

        damage = self.value
        card.health -= damage
        if card.health < 0:
            card.health = 0

        return [
            t(
                guild_id,
                "effect.burn.tick",
                name=card.name,
                damage=damage,
                source=self.description,
            )
        ]
