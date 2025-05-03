class Effect:
    def __init__(self, name, duration, effect_type, value, flat_bonus = 0, description=""):
        self.name = name
        self.duration = duration
        self.effect_type = effect_type
        self.value = value
        self.flat_bonus = flat_bonus 
        self.description = description

    def apply(self, card):
        logs = []
        if self.name == "Burn":
            card.health -= self.value
            if card.health < 0:
                card.health = 0
            logs.append(f"🔥 {card.name} chịu {self.value} sát thương từ burn.")
        return logs

    def on_expire(self, card):
        return [f"⏳ {self.description} trên {card.name} đã hết hiệu lực."]
    
    def on_receive_damage(self, card, damage):
        if self.name == "Immune":
            return 0, f"🛡️ {card.name} miễn nhiễm sát thương!"
        return damage, None
