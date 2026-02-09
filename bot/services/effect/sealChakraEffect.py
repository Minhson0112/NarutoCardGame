from bot.services.effectBase import Effect
from bot.services.i18n import t


class SealChakraEffect(Effect):
    def __init__(self, duration, description=""):
        super().__init__(
            name="SealChakra",
            duration=duration,
            effect_type="debuff",
            value=None,
            flat_bonus=0,
            description=description,
        )

    def apply(self, card):
        guild_id = getattr(card, "guild_id", None)
        return [
            t(
                guild_id,
                "effect.sealchakra.active",
                card_name=card.name,
            )
        ]

    def on_expire(self, card):
        guild_id = getattr(card, "guild_id", None)

        return [
            t(
                guild_id,
                "effect.sealchakra.expired",
                effect_desc=self.description,
                card_name=card.name,
            )
        ]
