from bot.config.database import getDbSession
from bot.entity.cardTemplate import CardTemplate

def seed_test_data():
    test_cards = [
        {
            "card_key": "sakura",
            "name": "Haruno Sakura",
            "tier": "Genin",
            "element": "Thủy",
            "health": 1200,
            "armor": 20,
            "base_damage": 80,
            "crit_rate": 0.1,
            "speed": 0.05,
            "chakra": 0,
            "first_position": False,
            "image_url": "sakura",
            "sell_price": 100
        },
        {
            "card_key": "neji",
            "name": "Hyuga Neji",
            "tier": "Chunin",
            "element": "Thể",
            "health": 1500,
            "armor": 30,
            "base_damage": 120,
            "crit_rate": 0.15,
            "speed": 0.1,
            "chakra": 0,
            "first_position": True,
            "image_url": "neji",
            "sell_price": 500
        },
        {
            "card_key": "konan",
            "name": "Konan",
            "tier": "Jounin",
            "element": "Phong",
            "health": 2500,
            "armor": 50,
            "base_damage": 200,
            "crit_rate": 0.2,
            "speed": 0.15,
            "chakra": 20,
            "first_position": False,
            "image_url": "konan",
            "sell_price": 2000
        },
        {
            "card_key": "tsunade",
            "name": "Tsunade",
            "tier": "Kage",
            "element": "Thủy",
            "health": 5000,
            "armor": 100,
            "base_damage": 350,
            "crit_rate": 0.1,
            "speed": 0.05,
            "chakra": 0,
            "first_position": True,
            "image_url": "tsunade",
            "sell_price": 10000
        },
        {
            "card_key": "naruto",
            "name": "Uzumaki Naruto",
            "tier": "Legendary",
            "element": "Phong",
            "health": 10000,
            "armor": 150,
            "base_damage": 600,
            "crit_rate": 0.25,
            "speed": 0.2,
            "chakra": 40,
            "first_position": False,
            "image_url": "naruto",
            "sell_price": 50000
        }
    ]

    with getDbSession() as session:
        for card_data in test_cards:
            existing = session.query(CardTemplate).filter_by(card_key=card_data["card_key"]).first()
            if existing:
                # Update
                for key, value in card_data.items():
                    setattr(existing, key, value)
            else:
                # Insert
                new_card = CardTemplate(**card_data)
                session.add(new_card)
        
        session.commit()
        print("✅ Đã khởi tạo dữ liệu mẫu thành công!")

if __name__ == "__main__":
    seed_test_data()
