from typing import Optional, Tuple

def get_card_effective_stats(card):
    """
    Trả về dict với các chỉ số đã được buff theo cấp độ:
      - strength: base_damage × cấp độ
      - các chỉ số khác (nếu có): ví dụ hp, armor… × (1 + 0.1*(level-1))
    """
    lvl = card.level or 1
    # độ tăng 10% cho mỗi cấp sau cấp 1
    multiplier = 1 + 0.1 * (lvl - 1)

    base = card.template
    # strength = base_damage × level × buff
    strength = int(base.base_damage * multiplier)

    # Buff các chỉ số khác nếu template có trường đó
    hp        = int(base.health * multiplier)
    armor     = int(base.armor * multiplier)
    crit_rate = base.crit_rate * multiplier
    speed     = base.speed * multiplier
    chakra    = int(base.chakra * multiplier)

    return {
        "strength":   strength,
        "hp":         hp,
        "armor":      armor,
        "crit_rate":  crit_rate,
        "speed":      speed,
        "chakra":     chakra,
    }


def get_weapon_effective_stats(weapon):
    """
    Trả về dict với các bonus_* đã buff theo cấp độ:
      - Những trường None sẽ được giữ None
      - Các trường có giá trị sẽ × (1 + 0.1*(level-1))
    """
    lvl = weapon.level or 1
    multiplier = 1 + 0.1 * (lvl - 1)

    tmpl = weapon.template
    def buff(attr):
        v = getattr(tmpl, attr)
        if v is None:
            return None
        new = v * multiplier
        return int(new) if isinstance(v, int) else new

    return {
        "bonus_health":     buff("bonus_health"),
        "bonus_armor":      buff("bonus_armor"),
        "bonus_damage":     buff("bonus_damage"),
        "bonus_crit_rate":  buff("bonus_crit_rate"),
        "bonus_speed":      buff("bonus_speed"),
        "bonus_chakra":     buff("bonus_chakra"),
    }

def get_battle_card_params(
    player_card,                      # instance PlayerCard
    player_weapon: Optional[object] = None,  # instance PlayerWeapon hoặc None
) -> Tuple[str, int, int, int, float, float, int, str, str]:
    """
    Trả về tuple:
      (name, health, armor, base_damage, crit_rate, speed, chakra, position, element, tier)
    đã bao gồm level‑buff của thẻ và bonus từ vũ khí (nếu có).
    """
    # 1) Lấy stats thẻ đã buff theo cấp độ
    stats = get_card_effective_stats(player_card)

    # 2) Nếu có vũ khí, cộng thêm từng bonus_* đã buff
    if player_weapon:
        wstats = get_weapon_effective_stats(player_weapon)
        stats["hp"]       += wstats.get("bonus_health")    or 0
        stats["armor"]    += wstats.get("bonus_armor")     or 0
        stats["strength"] += wstats.get("bonus_damage")    or 0
        stats["crit_rate"]+= wstats.get("bonus_crit_rate") or 0
        stats["speed"]    += wstats.get("bonus_speed")     or 0
        stats["chakra"]   += wstats.get("bonus_chakra")    or 0



    # 4) Trả về tuple đúng tham số của create_card()
    return (
        player_card.template.name,
        stats["hp"],
        stats["armor"],
        stats["strength"],
        stats["crit_rate"],
        stats["speed"],
        stats["chakra"],
        player_card.template.element,
        player_card.template.tier
    )