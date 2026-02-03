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
    
    def getRandomTailedCard(self) -> List[Optional[CardTemplate]]:
        tailedTier = ["1vi", "2vi", "3vi", "4vi", "5vi", "6vi", "7vi", "8vi", "9vi"]
        return [self.session.query(CardTemplate).filter_by(tier=(random.choice(tailedTier))).first()]
    
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

    def getByName(self, name: str) -> Optional[CardTemplate]:
        """
        Lấy card template theo name (dùng cho /showcard).
        """
        return (
            self.session
            .query(CardTemplate)
            .filter_by(name=name)
            .first()
        )

    def searchNamesForAutocomplete(self, typed: str, limit: int = 25) -> List[str]:
        """
        Trả về danh sách tên thẻ phục vụ autocomplete.
        Ưu tiên match prefix trước, nếu chưa đủ thì bổ sung match contains.
        """
        typed = (typed or "").strip()
        if not typed:
            return []

        prefix_rows = (
            self.session
            .query(CardTemplate.name)
            .filter(CardTemplate.name.like(f"{typed}%"))
            .order_by(CardTemplate.name.asc())
            .limit(limit)
            .all()
        )
        names = [r[0] for r in prefix_rows]

        if len(names) < limit:
            remaining = limit - len(names)
            contains_rows = (
                self.session
                .query(CardTemplate.name)
                .filter(CardTemplate.name.like(f"%{typed}%"))
                .order_by(CardTemplate.name.asc())
                .limit(remaining)
                .all()
            )
            for r in contains_rows:
                if r[0] not in names:
                    names.append(r[0])
                    if len(names) >= limit:
                        break

        return names