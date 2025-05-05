from bot.services.cardBase import Card

class AkimichiChoji(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🍡 {self.name} uống thuốc Ba Màu, biến thành khổng lồ!")

        # Hồi lại 50% máu đã mất
        missing_hp = self.max_health - self.health
        heal_amount = int(missing_hp * 0.5)
        if heal_amount > 0:
            logs.extend(self.receive_healing(amount=heal_amount))
        else:
            logs.append(f"💚 {self.name} đang đầy máu, không cần hồi phục.")

        # Giải toàn bộ hiệu ứng debuff
        removed_effects = [e for e in self.effects if e.effect_type == "debuff"]
        for effect in removed_effects:
            logs.append(f"🧹 {self.name} loại bỏ hiệu ứng: {effect.description}.")
            self.effects.remove(effect)

        if not removed_effects:
            logs.append(f"✅ {self.name} không có hiệu ứng bất lợi nào để giải.")

        return logs