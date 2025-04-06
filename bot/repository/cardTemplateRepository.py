import random
from bot.entity.cardTemplate import CardTemplate

class CardTemplateRepository:
    def __init__(self, session):
        self.session = session

    def getByKey(self, cardKey: str) -> CardTemplate:
        """
        Lấy card template theo card_key.
        """
        return self.session.query(CardTemplate).filter_by(card_key=cardKey).first()

    def getAllByTier(self, tier: str):
        """
        Lấy danh sách tất cả card template theo tier.
        """
        return self.session.query(CardTemplate).filter_by(tier=tier).all()

    def getRandomByTier(self, tier: str) -> CardTemplate:
        """
        Trả về ngẫu nhiên một card template có tier được chỉ định.
        """
        cards = self.getAllByTier(tier)
        if cards:
            return random.choice(cards)
        return None
