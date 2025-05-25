from bot.services.cardBase import Card
from bot.services.effect.immuneEffect import ImmuneEffect
from bot.services.effect.illusionEffect import IllusionEffect

class SenjuHashirama(Card):
    def special_skills(self):
        logs: list[str] = []
        logs.append(f"🌳 {self.name} triệu hồi phật nghìn tay: hồi phục, giải trừ và bảo hộ toàn đội!")

        # ---  Xác định nhóm "đồng minh thực" ---
        if any(isinstance(e, IllusionEffect) for e in self.effects):
            real_allies = self.enemyTeam
        else:
            real_allies = self.team

        # --- 1️⃣ Giải trừ mọi debuff trên nhóm đồng minh thực ---
        for ally in real_allies:
            if not ally.is_alive():
                continue
            expired_logs = []
            # gom lại các effect_type=='debuff'
            remaining = []
            for e in ally.effects:
                if e.effect_type == "debuff":
                    # gọi on_expire để restore state nếu cần (vd: Illusion sẽ swap back)
                    expired_logs.extend(e.on_expire(ally))
                else:
                    remaining.append(e)
            ally.effects = remaining
            # append log
            for ln in expired_logs:
                logs.append(f"❎ {ln}")

        # --- 2️⃣ Hồi máu 500% SMKK ---
        heal_amount = int(self.get_effective_base_damage() * 5)
        for ally in real_allies:
            if ally.is_alive():
                logs.extend(ally.receive_healing(amount=heal_amount))

        # --- 3️⃣ Cấp miễn nhiễm sát thương trong 1 lượt ---
        for ally in real_allies:
            if ally.is_alive():
                immune = ImmuneEffect(
                    duration=1,
                    description=f"Miễn nhiễm sát thương từ phật nghìn tay của {self.name}"
                )
                ally.effects.append(immune)
                logs.append(f"🛡️ {ally.name} được miễn nhiễm sát thương trong 2 lượt!")

        return logs
