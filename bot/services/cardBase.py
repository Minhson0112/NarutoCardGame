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

    def receive_damage(self, damage, true_damage=False, execute_threshold=None):
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

        # hiệu ứng kết liễu % máu
        if execute_threshold is not None:
            hp_ratio = self.health / self.max_health if self.max_health else 0
            if self.is_alive() and hp_ratio <= execute_threshold:
                self.health = 0
                logs.append(f"💀 {self.name} bị kết liễu do HP xuống dưới {int(execute_threshold * 100)}% sau đòn đánh.")

        return dealt_damage, logs
    
    def receive_healing(self, amount=None, percent_of_max=None):
        """
        Hồi máu cho thẻ:
        - amount: số máu hồi trực tiếp (ví dụ 500)
        - percent_of_max: hồi theo % máu tối đa (ví dụ 0.1 = 10%)
        """
        logs = []
        if amount is None and percent_of_max is None:
            logs.append(f"⚠️ Không có giá trị hồi máu hợp lệ được truyền vào.")
            return logs

        healing = 0
        if percent_of_max is not None:
            healing += int(self.max_health * percent_of_max)
        if amount is not None:
            healing += amount

        if healing <= 0:
            logs.append(f"{self.name} không hồi được máu nào.")
            return logs

        old_health = self.health
        self.health = min(self.max_health, self.health + healing)
        actual_healed = self.health - old_health

        logs.append(f"💚 {self.name} hồi {actual_healed} HP.")
        return logs
    
    def receive_armor_buff(self, armor_increase: int):
        """
        Tăng giáp trực tiếp (buff tức thời, không phải hiệu ứng theo lượt).
        
        Args:
            armor_increase (int): Số giáp cộng thêm ngay lập tức.
            
        Returns:
            list[str]: Log hiển thị thông tin buff.
        """
        self.armor += armor_increase
        return [f"🛡️ {self.name} nhận buff +{armor_increase} giáp (hiện tại: {self.armor})."]
    
    def receive_crit_buff(self, crit_increase: float):
        """
        Tăng chí mạng trực tiếp (buff tức thời, không phải hiệu ứng theo lượt).

        Args:
            crit_increase (float): Tăng thêm % chí mạng (ví dụ 0.1 = +10%).
            
        Returns:
            list[str]: Log hiển thị thông tin buff.
        """
        before = self.crit_rate
        self.crit_rate += crit_increase
        # Clamp lại để không vượt quá 100%
        if self.crit_rate > 1.0:
            self.crit_rate = 1.0
        return [
            f"💥 {self.name} nhận buff +{crit_increase*100:.0f}% chí mạng "
            f"(từ {before*100:.0f}% lên {self.crit_rate*100:.0f}%)."
        ]
    
    def receive_speed_buff(self, speed_increase: float):
        """
        Tăng speed trực tiếp (buff tức thời, không phải hiệu ứng theo lượt).
        Speed ảnh hưởng đến tỷ lệ né tránh (%).

        Args:
            speed_increase (float): Tăng thêm % speed (ví dụ 0.1 = +10%).
            
        Returns:
            list[str]: Log hiển thị thông tin buff.
        """
        before = self.speed
        self.speed += speed_increase
        if self.speed > 0.7:
            self.speed = 0.7  # Clamp tối đa 70%

        return [
            f"🏃 {self.name} nhận buff +{speed_increase*100:.0f}% speed "
            f"(từ {before*100:.0f}% lên {self.speed*100:.0f}%)."
        ]
    
    def receive_chakra_buff(self, chakra_increase: int):
        """
        Tăng chakra trực tiếp (buff tức thời, không phải hiệu ứng theo lượt).

        Args:
            chakra_increase (int): Số chakra được cộng thêm.
            
        Returns:
            list[str]: Log hiển thị thông tin buff.
        """
        before = self.chakra
        self.chakra += chakra_increase
        if self.chakra > 100:
            self.chakra = 100  # Clamp tối đa 100 (nếu game bạn dùng kiểu này)

        return [
            f"🔋 {self.name} nhận buff +{chakra_increase} chakra "
            f"(từ {before} lên {self.chakra})."
        ]


    def reduce_armor_direct(self, armor_reduce: int = 0, percent_reduce: float = 0.0):
        """
        Giảm giáp trực tiếp (không qua hiệu ứng theo lượt).

        Args:
            armor_reduce (int): Số giáp giảm trực tiếp (ví dụ: 50).
            percent_reduce (float): Tỷ lệ % giảm giáp (ví dụ: 0.3 = giảm 30% giáp hiện tại).

        Returns:
            list[str]: Log thông tin giảm giáp.
        """
        before = self.armor

        # Tính toán giảm theo % nếu có
        percent_amount = int(self.armor * percent_reduce) if percent_reduce > 0 else 0

        # Tổng giảm
        total_reduce = armor_reduce + percent_amount

        self.armor -= total_reduce
        if self.armor < 0:
            self.armor = 0

        return [f"🛡️ {self.name} bị giảm trực tiếp {total_reduce} giáp (từ {before} xuống {self.armor})."]

    
    def reduce_crit_direct(self, crit_reduce: float):
        """
        Giảm chí mạng trực tiếp (không qua hiệu ứng theo lượt).

        Args:
            crit_reduce (float): Giảm % crit (ví dụ 0.1 = giảm 10%).
            
        Returns:
            list[str]: Log thông tin giảm crit.
        """
        before = self.crit_rate
        self.crit_rate -= crit_reduce
        if self.crit_rate < 0.0:
            self.crit_rate = 0.0
        return [
            f"💥 {self.name} bị giảm trực tiếp {crit_reduce*100:.0f}% chí mạng "
            f"(từ {before*100:.0f}% xuống {self.crit_rate*100:.0f}%)."
        ]

    def reduce_speed_direct(self, speed_reduce: float):
        """
        Giảm speed trực tiếp (ảnh hưởng né tránh, không qua hiệu ứng theo lượt).

        Args:
            speed_reduce (float): Giảm % speed (ví dụ 0.1 = giảm 10%).
            
        Returns:
            list[str]: Log thông tin giảm speed.
        """
        before = self.speed
        self.speed -= speed_reduce
        if self.speed < 0.0:
            self.speed = 0.0
        return [
            f"🏃 {self.name} bị giảm trực tiếp {speed_reduce*100:.0f}% speed "
            f"(từ {before*100:.0f}% xuống {self.speed*100:.0f}%)."
        ]
    
    def reduce_chakra_direct(self, chakra_reduce: int):
        """
        Giảm chakra trực tiếp (không qua hiệu ứng theo lượt).

        Args:
            chakra_reduce (int): Giảm bao nhiêu chakra.
            
        Returns:
            list[str]: Log thông tin giảm chakra.
        """
        before = self.chakra
        self.chakra -= chakra_reduce
        if self.chakra < 0:
            self.chakra = 0
        return [
            f"🔋 {self.name} bị giảm trực tiếp {chakra_reduce} chakra "
            f"(từ {before} xuống {self.chakra})."
        ]
    
    def health_bar(self, bar_length=20):
        ratio = self.health / self.max_health if self.max_health else 0
        filled = int(ratio * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        return f"HP: [{bar}] {self.health}/{self.max_health}"


