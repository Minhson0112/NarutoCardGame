import random
from bot.entity.cardTemplate import CardTemplate
from typing import List, Optional

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
    def getRandomByTierAndPosition(
        self, tier: str, first_position: bool) -> Optional[CardTemplate]:
        cards = (
            self.session
            .query(CardTemplate)
            .filter_by(tier=tier, first_position=first_position)
            .all()
        )
        return random.choice(cards) if cards else None

    def getFormationTemplates(self) -> List[Optional[CardTemplate]]:

        tiers = ['Chunin', 'Jounin', 'Kage', 'Legendary']

        # Slot 0: first_position=True
        tier0 = random.choice(tiers)
        slot0 = self.getRandomByTierAndPosition(tier0, True)

        # Slot 1 & 2: first_position=False, không trùng nhau
        selected_keys = set()
        slots = []
        for _ in range(2):
            card = None
            # thử cho đến khi chọn được card_key chưa xuất hiện trong selected_keys
            while True:
                tier_i = random.choice(tiers)
                candidate = self.getRandomByTierAndPosition(tier_i, False)
                if not candidate:
                    # nếu không còn card nào thỏa mãn, thoát vòng
                    break
                if candidate.card_key not in selected_keys:
                    card = candidate
                    selected_keys.add(candidate.card_key)
                    break
            slots.append(card)

        return [slot0] + slots