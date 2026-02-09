from bot.services.i18n import t

class Effect:
    def __init__(self, name, duration, effect_type, value, flat_bonus=0, description=""):
        self.name = name
        self.duration = duration
        self.effect_type = effect_type
        self.value = value
        self.flat_bonus = flat_bonus
        self.description = description
        self.trigger_on_pre_action = False

    def apply(self, card):
        logs = []
        return logs

    def on_expire(self, card):
        guild_id = getattr(card, "guild_id", None)
        return [
            t(
                guild_id,
                "effect.expired",
                effect_desc=self.description,
                card_name=card.name,
            )
        ]
