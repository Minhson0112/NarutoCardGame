from typing import Optional, Tuple

def get_card_effective_stats(card):
    """
    Trả về dict với các chỉ số đã được buff theo cấp độ và theo bậc thẻ:
      - strength, hp, armor, crit_rate, speed, chakra đều được nhân với multiplier
      - multiplier = 1 + tier_rate * (level - 1)
    Tier rate:
      - Genin:      30%  mỗi cấp
      - Chunin:     25%  mỗi cấp
      - Jounin:     20%  mỗi cấp
      - Kage:       15%  mỗi cấp
      - Legendary:  10%  mỗi cấp (giữ nguyên)
    """
    lvl = card.level or 1

    # Định nghĩa tỉ lệ buff theo từng tier
    buff_rates = {
        "Genin":     0.30,
        "Chunin":    0.25,
        "Jounin":    0.20,
        "Kage":      0.15,
        "Legendary": 0.10,
    }
    tier = card.template.tier
    tier_rate = buff_rates.get(tier, 0.10)  # nếu không tìm thấy thì mặc định 10%

    # multiplier = 1 + tier_rate × (level - 1)
    multiplier = 1 + tier_rate * (lvl - 1)

    base = card.template
    return {
        "strength":  int(base.base_damage * multiplier),
        "hp":        int(base.health     * multiplier),
        "armor":     int(base.armor      * multiplier),
        "crit_rate": base.crit_rate      * multiplier,
        "speed":     base.speed          * multiplier,
        "chakra":    int(base.chakra     * multiplier),
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