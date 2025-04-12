from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from bot.config.database import Base

class Challenge(Base):
    __tablename__ = 'challenges'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_name = Column(String(100), nullable=False)
    card_strength = Column(Integer, nullable=False)
    image_url_key = Column(String(255), nullable=False)
    narrative = Column(Text)
    bonus_ryo = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    
    def __repr__(self):
        return (f"<Challenge(id={self.id}, card_name='{self.card_name}', "
                f"card_strength={self.card_strength}, bonus_ryo={self.bonus_ryo})>")
