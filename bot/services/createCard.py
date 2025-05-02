from bot.services.cardBase import Card
from bot.services.fireCard import FireCard
from bot.services.windCard import WindCard
from bot.services.waterCard import WaterCard
from bot.services.taijutsuCard import TaijutsuCard
from bot.services.lightningCard import LightningCard
from bot.services.earthCard import EarthCard
from bot.services.tailedCard import TailedBeastCard

ELEMENT_CLASS_MAP = {
    "Hỏa": FireCard,
    "Thủy": WaterCard,
    "Thổ": EarthCard,
    "Phong": WindCard,
    "Lôi": LightningCard,
    "Thể": TaijutsuCard,
    "vi": TailedBeastCard
}

def create_card(name, health, armor, base_damage, crit_rate, speed, chakra, element, tier):
    card_class = ELEMENT_CLASS_MAP.get(element, Card)
    return card_class(name, health, armor, base_damage, crit_rate, speed, chakra, element, tier)
