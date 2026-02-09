from bot.services.effectBase import Effect
from bot.services.i18n import t


class Card:
    def __init__(
        self,
        name,
        health,
        armor,
        base_damage,
        crit_rate,
        speed,
        chakra,
        element,
        tier,
        level,
        weapon_passive,
        guild_id=None,
    ):
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
        self.level = level

        self.guild_id = guild_id

        self.target = None
        self.team = None
        self.enemyTeam = None

        self.effects: list[Effect] = []
        self.passives: list[Effect] = []
        if weapon_passive:
            self.passives.append(weapon_passive)

    def set_guild_id(self, guild_id) -> None:
        self.guild_id = guild_id

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

    def has_passives_effect(self, effect_name):
        return any(effect.name == effect_name for effect in self.passives)

    def has_buff(self):
        return any(e.effect_type == "buff" for e in self.effects)

    def has_debuff(self):
        return any(e.effect_type == "debuff" for e in self.effects)

    def process_effects(self):
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

    def process_pre_action_effects(self):
        logs = []
        for effect in self.effects:
            if getattr(effect, "trigger_on_pre_action", False):
                logs.extend(effect.apply(self))
        return logs

    def receive_damage(self, damage, true_damage=False, execute_threshold=None, attacker=None):
        logs = []

        if self.has_effect("Immune"):
            logs.append(t(self.guild_id, "card.damage.immune", name=self.name))
            return 0, logs

        if damage == 0:
            return 0, logs

        if true_damage:
            self.health -= damage
            if self.health < 0:
                self.health = 0
            logs.append(t(self.guild_id, "card.damage.true", name=self.name, damage=damage))
            dealt_damage = damage
        else:
            dealt_damage = max(damage - self.get_effective_armor(), 0)
            self.health -= dealt_damage
            if self.health < 0:
                self.health = 0
            logs.append(t(self.guild_id, "card.damage.normal", name=self.name, damage=dealt_damage))

        if self.max_health:
            percent_lost = dealt_damage / self.max_health
            gained_chakra = int(percent_lost * 100)
            if gained_chakra > 0:
                logs.extend(self.receive_chakra_buff(gained_chakra))

        if execute_threshold is not None:
            hp_ratio = self.health / self.max_health if self.max_health else 0
            if self.is_alive() and hp_ratio <= execute_threshold:
                self.health = 0
                logs.append(
                    t(
                        self.guild_id,
                        "card.execute",
                        name=self.name,
                        threshold_percent=int(execute_threshold * 100),
                    )
                )

        if attacker and dealt_damage > 0 and self.health == 0:
            logs.extend(attacker.receive_chakra_buff(20))

        if attacker and dealt_damage > 0 and self.has_effect("Reflect"):
            reflect_effect = next((e for e in self.effects if e.name == "Reflect"), None)
            if reflect_effect is not None:
                reflect_percent = max(0, reflect_effect.value)
                reflect_damage = int(dealt_damage * reflect_percent)
                if reflect_damage > 0:
                    attacker.health -= reflect_damage
                    if attacker.health < 0:
                        attacker.health = 0
                    logs.append(
                        t(
                            self.guild_id,
                            "card.reflect",
                            attacker_name=attacker.name,
                            reflect_damage=reflect_damage,
                            reflect_percent=int(reflect_percent * 100),
                            dealt_damage=dealt_damage,
                        )
                    )

        if self.health == 0:
            for p in list(self.passives):
                if p.name == "protection":
                    logs.extend(p.apply(self))

        if self.health > 0 and self.max_health and self.health / self.max_health <= 0.2:
            for p in list(self.passives):
                if p.name == "armorProtection":
                    logs.extend(p.apply(self))

        if attacker and attacker.has_passives_effect("lifeSteal"):
            steal = int(dealt_damage * 0.2)
            if steal > 0:
                logs.extend(attacker.receive_healing(amount=steal))

        return dealt_damage, logs

    def receive_healing(self, amount=None, percent_of_max=None):
        logs = []
        if amount is None and percent_of_max is None:
            logs.append(t(self.guild_id, "card.heal.invalid_input"))
            return logs

        healing = 0
        if percent_of_max is not None:
            healing += int(self.max_health * percent_of_max)

        if amount is not None:
            for effect in self.effects:
                if effect.name == "AntiHeal":
                    amount = int(amount * effect.value)
                    logs.append(
                        t(
                            self.guild_id,
                            "card.heal.antiheal_applied",
                            name=self.name,
                            effect_desc=effect.description,
                        )
                    )
                    break
            healing += amount

        if healing <= 0:
            logs.append(t(self.guild_id, "card.heal.no_heal", name=self.name))
            return logs

        old_health = self.health
        self.health = min(self.max_health, self.health + healing)
        actual_healed = self.health - old_health

        logs.append(t(self.guild_id, "card.heal.success", name=self.name, healed=actual_healed))
        return logs

    def receive_base_damage_buff(self, damage_increase: int):
        self.base_damage += damage_increase
        return [
            t(
                self.guild_id,
                "card.buff.base_damage",
                name=self.name,
                amount=damage_increase,
                current=self.base_damage,
            )
        ]

    def receive_armor_buff(self, armor_increase: int):
        self.armor += armor_increase
        return [
            t(
                self.guild_id,
                "card.buff.armor",
                name=self.name,
                amount=armor_increase,
                current=self.armor,
            )
        ]

    def receive_crit_buff(self, crit_increase: float):
        before = self.crit_rate
        self.crit_rate += crit_increase
        if self.crit_rate > 1.0:
            self.crit_rate = 1.0

        return [
            t(
                self.guild_id,
                "card.buff.crit",
                name=self.name,
                percent=int(crit_increase * 100),
                before=int(before * 100),
                after=int(self.crit_rate * 100),
            )
        ]

    def receive_speed_buff(self, speed_increase: float):
        before = self.speed
        self.speed += speed_increase
        if self.speed > 0.7:
            self.speed = 0.7

        return [
            t(
                self.guild_id,
                "card.buff.speed",
                name=self.name,
                percent=int(speed_increase * 100),
                before=int(before * 100),
                after=int(self.speed * 100),
            )
        ]

    def receive_chakra_buff(self, chakra_increase: int):
        if self.has_effect("SealChakra"):
            return [t(self.guild_id, "card.chakra.sealed", name=self.name)]

        self.chakra += chakra_increase
        return [t(self.guild_id, "card.chakra.gain", name=self.name, amount=chakra_increase)]

    def reduce_armor_direct(self, armor_reduce: int = 0, percent_reduce: float = 0.0):
        before = self.armor
        percent_amount = int(self.armor * percent_reduce) if percent_reduce > 0 else 0
        total_reduce = armor_reduce + percent_amount

        self.armor -= total_reduce
        if self.armor < 0:
            self.armor = 0

        return [
            t(
                self.guild_id,
                "card.reduce.armor",
                name=self.name,
                amount=total_reduce,
                before=before,
                after=self.armor,
            )
        ]

    def reduce_crit_direct(self, crit_reduce: float):
        before = self.crit_rate
        self.crit_rate -= crit_reduce
        if self.crit_rate < 0.0:
            self.crit_rate = 0.0

        return [
            t(
                self.guild_id,
                "card.reduce.crit",
                name=self.name,
                percent=int(crit_reduce * 100),
                before=int(before * 100),
                after=int(self.crit_rate * 100),
            )
        ]

    def reduce_speed_direct(self, speed_reduce: float):
        before = self.speed
        self.speed -= speed_reduce
        if self.speed < 0.0:
            self.speed = 0.0

        return [
            t(
                self.guild_id,
                "card.reduce.speed",
                name=self.name,
                percent=int(speed_reduce * 100),
                before=int(before * 100),
                after=int(self.speed * 100),
            )
        ]

    def reduce_chakra_direct(self, chakra_reduce: int):
        before = self.chakra
        self.chakra -= chakra_reduce
        if self.chakra < 0:
            self.chakra = 0

        return [
            t(
                self.guild_id,
                "card.reduce.chakra",
                name=self.name,
                amount=chakra_reduce,
                before=before,
                after=self.chakra,
            )
        ]

    def health_bar(self, bar_length=20):
        ratio = self.health / self.max_health if self.max_health else 0
        filled = int(ratio * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        return t(
            self.guild_id,
            "card.hp_bar",
            bar=bar,
            hp=self.health,
            max_hp=self.max_health,
        )
