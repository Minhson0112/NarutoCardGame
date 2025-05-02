class Card:
    def __init__(self, name, health, armor, base_damage, crit_rate, speed, chakra, element, tier):
        self.name = name
        self.health = health
        self.max_health = health
        self.armor = armor
        self.base_damage = base_damage
        self.crit_rate = crit_rate
        self.speed = speed
        self.chakra = chakra
        self.element = element
        self.tier = tier
        self.target = None
        self.team = None
        self.enemyTeam = None
        self.effects: list = []

    def get_effective_base_damage(self):
        multiplier = 1.0
        flat_bonus = 0
        for effect in self.effects:
            if effect.name == "BuffDamage":
                multiplier *= (1 + effect.value)
                flat_bonus += effect.flat_bonus
            elif effect.name == "DebuffDamage":
                multiplier *= (1 - effect.value)
                flat_bonus -= effect.flat_bonus
        result = self.base_damage * multiplier + flat_bonus
        return max(1, int(result))

    def get_effective_armor(self):
        multiplier = 1.0
        flat_bonus = 0
        for effect in self.effects:
            if effect.name == "BuffArmor":
                multiplier *= (1 + effect.value)
                flat_bonus += effect.flat_bonus
            elif effect.name == "DebuffArmor":
                multiplier *= (1 - effect.value)
                flat_bonus -= effect.flat_bonus
        result = self.armor * multiplier + flat_bonus
        return max(0, int(result))
    
    def get_effective_crit_rate(self):
        multiplier = 1.0
        flat_bonus = 0
        for effect in self.effects:
            if effect.name == "BuffCrit":
                multiplier *= (1 + effect.value)
                flat_bonus += effect.flat_bonus
            elif effect.name == "DebuffCrit":
                multiplier *= (1 - effect.value)
                flat_bonus -= effect.flat_bonus
        result = self.crit_rate * multiplier + flat_bonus
        return max(0.0, min(1.0, result))

    def get_effective_speed(self):
        multiplier = 1.0
        flat_bonus = 0
        for effect in self.effects:
            if effect.name == "BuffSpeed":
                multiplier *= (1 + effect.value)
                flat_bonus += effect.flat_bonus
            elif effect.name == "DebuffSpeed":
                multiplier *= (1 - effect.value)
                flat_bonus -= effect.flat_bonus
        result = self.speed * multiplier + flat_bonus
        return max(0.0, min(0.7, result))
    
    def is_alive(self):
        return self.health > 0
    
    def has_effect(self, effect_name):
        return any(effect.name == effect_name for effect in self.effects)
    
    def has_buff(self):
        return any(e.effect_type == 'buff' for e in self.effects)

    def has_debuff(self):
        return any(e.effect_type == 'debuff' for e in self.effects)
    
    def process_effects(self):
        """Xử lý tất cả hiệu ứng đang có (ví dụ burn, stun...)"""
        logs = []
        expired_effects = []

        for effect in self.effects:
            logs.extend(effect.apply(self))
            effect.duration -= 1
            if effect.duration <= 0:
                expired_effects.append(effect)

        for effect in expired_effects:
            logs.extend(effect.on_expire(self))
            self.effects.remove(effect)

        return logs

    def receive_damage(self, damage, true_damage=False):
        """
        Nhận sát thương:
        - damage: số damage gây ra
        - true_damage: nếu True → bỏ qua giáp (sát thương chuẩn)
        """
        logs = []

        # Hook hiệu ứng miễn nhiễm
        for effect in self.effects:
            if hasattr(effect, "on_receive_damage"):
                new_damage, log = effect.on_receive_damage(self, damage)
                if log:
                    logs.append(log)
                damage = new_damage

        if damage == 0:
            return 0, logs

        if true_damage:
            # Sát thương chuẩn: bỏ qua giáp
            self.health -= damage
            if self.health < 0:
                self.health = 0
            logs.append(f" {self.name} nhận {damage} sát thương chuẩn (bỏ qua giáp).")
            return damage, logs

        # Áp dụng giáp
        dealt_damage = max(damage - self.armor, 0)
        self.health -= dealt_damage
        if self.health < 0:
            self.health = 0
        logs.append(f"{self.name} nhận {dealt_damage} sát thương.")
        return dealt_damage, logs
    
    def health_bar(self, bar_length=20):
        ratio = self.health / self.max_health if self.max_health else 0
        filled = int(ratio * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        return f"HP: [{bar}] {self.health}/{self.max_health}"


