from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, text, Enum, Boolean, Float
from bot.config.database import Base

class CardTemplate(Base):
    __tablename__ = 'card_templates'

    card_key = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)

    tier = Column(Enum('Genin', 'Chunin', 'Jounin', 'Kage', 'Legendary', name="card_tier_enum"), nullable=False)
    element = Column(String(20))  # Phong, Lôi, Thổ, Thủy, Hỏa, Thể

    # === Các chỉ số cơ bản để scale lên khi chiến đấu ===
    health = Column(Integer, nullable=False, default=1000)
    armor = Column(Integer, nullable=False, default=10)
    base_damage = Column(Integer, nullable=False, default=50)
    crit_rate = Column(Float, nullable=False, default=0.1)  # 10%
    speed = Column(Float, nullable=False, default=0.05)     # 5% dodge
    chakra = Column(Integer, nullable=False, default=0)     # khởi điểm

    first_position = Column(Boolean, nullable=False, default=False)  # True = bắt buộc đứng hàng đầu

    image_url = Column(Text)
    sell_price = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return f"<CardTemplate(card_key='{self.card_key}', name='{self.name}', tier='{self.tier}')>"
