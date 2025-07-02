class Effect:
    def __init__(self, name, duration, effect_type, value, flat_bonus = 0, description=""):
        self.name = name
        self.duration = duration
        self.effect_type = effect_type
        self.value = value #boo
        self.flat_bonus = flat_bonus # int
        self.description = description
        self.trigger_on_pre_action = False

    def apply(self, card):
        logs = []
        return logs

    def on_expire(self, card):
        return [f"⏳ {self.description} trên {card.name} đã hết hiệu lực."]
    
