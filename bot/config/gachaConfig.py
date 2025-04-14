# 🎴 Tên gói mở thẻ
GACHA_PACKS = ["card_basic", "card_advanced", "card_elite"]

# 🛡️ Bảo hiểm: Số lần mở tối đa trước khi đảm bảo nhận thẻ tối thiểu theo gói
PITY_LIMIT = {
    "card_basic": 20,
    "card_advanced": 10,
    "card_elite": 5
}

# 🛡️ Bậc tối thiểu được đảm bảo sau khi chạm mốc bảo hiểm
PITY_PROTECTION = {
    "card_basic": "Jounin",
    "card_advanced": "Kage",
    "card_elite": "Legendary"
}

# 💸 Giá mỗi gói
GACHA_PRICES = {
    "card_basic": 10000,
    "card_advanced": 100000,
    "card_elite": 1000000
}

# 🎲 Tỉ lệ rơi thẻ theo bậc
GACHA_DROP_RATE = {
    "card_basic": {
        "Genin": 75,
        "Chunin": 19,
        "Jounin": 5,
        "Kage": 0.9999,
        "Legendary": 0.0001
    },
    "card_advanced": {
        "Genin": 50,
        "Chunin": 29,
        "Jounin": 15,
        "Kage": 5,
        "Legendary": 1
    },
    "card_elite": {
        "Genin": 15,
        "Chunin": 30,
        "Jounin": 35,
        "Kage": 15,
        "Legendary": 5
    }
}
