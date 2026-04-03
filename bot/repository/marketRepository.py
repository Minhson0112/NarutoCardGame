from sqlalchemy import or_
from bot.entity.marketListing import MarketListing
from bot.entity.cardTemplate import CardTemplate
from datetime import datetime

class MarketRepository:
    def __init__(self, session):
        self.session = session

    def getById(self, listing_id: int) -> MarketListing:
        return self.session.query(MarketListing).filter_by(id=listing_id).first()

    def getActiveListings(self, tier: str = None, card_name: str = None, seller_id: int = None):
        query = self.session.query(MarketListing).filter(MarketListing.status == 'LISTED')
        
        if tier:
            query = query.join(CardTemplate).filter(CardTemplate.tier == tier)
        
        if card_name:
            if not tier: # Avoid double join
                query = query.join(CardTemplate)
            query = query.filter(CardTemplate.name.like(f"%{card_name}%"))
            
        if seller_id:
            query = query.filter(MarketListing.seller_id == seller_id)
            
        return query.order_by(MarketListing.created_at.desc()).all()

    def create(self, listing: MarketListing):
        self.session.add(listing)

    def update(self, listing: MarketListing):
        pass

    def getExpiredListings(self):
        now = datetime.now()
        return self.session.query(MarketListing).filter(
            MarketListing.status == 'LISTED',
            MarketListing.expires_at <= now
        ).all()
        
    def getPlayerListings(self, player_id: int):
        return self.session.query(MarketListing).filter(
            MarketListing.seller_id == player_id
        ).order_by(MarketListing.created_at.desc()).all()
