from bot.services.effectBase import Effect
from bot.services.i18n import t


class IllusionEffect(Effect):
    def __init__(self, duration, description=""):
        super().__init__(
            name="Illusion",
            duration=duration,
            effect_type="debuff",
            value=None,
            description=description,
        )
        self.original_team = None
        self.original_enemy_team = None
        self.trigger_on_pre_action = True
        self.is_swapped = False

    def apply(self, card):
        logs = []
        guild_id = getattr(card, "guild_id", None)

        if not self.is_swapped:
            self.original_team = card.team
            self.original_enemy_team = card.enemyTeam

            card.team, card.enemyTeam = card.enemyTeam, card.team

            self.is_swapped = True

            logs.append(
                t(
                    guild_id,
                    "effect.illusion.hit",
                    card_name=card.name,
                )
            )

        return logs

    def on_expire(self, card):
        logs = []
        guild_id = getattr(card, "guild_id", None)

        if self.is_swapped:
            card.team = self.original_team
            card.enemyTeam = self.original_enemy_team

            logs.append(
                t(
                    guild_id,
                    "effect.illusion.expired",
                    card_name=card.name,
                )
            )

        return logs
