from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, Enum, text
from bot.config.database import Base

class CardTemplate(Base):
    __tablename__ = 'card_templates'

    card_key = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    tier = Column(Enum('Genin', 'Chunin', 'Jounin', 'Kage', 'Legendary', name="card_tier_enum"), nullable=False)
    element = Column(String(20))
    base_power = Column(Integer)
    image_url = Column(Text)  # Lưu key để tra cứu trong CARD_IMAGE_MAP
    sell_price = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return f"<CardTemplate(card_key='{self.card_key}', name='{self.name}', tier='{self.tier}')>"
