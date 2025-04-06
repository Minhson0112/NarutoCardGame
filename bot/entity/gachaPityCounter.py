from sqlalchemy import Column, BigInteger, String, Integer
from bot.config.database import Base

class GachaPityCounter(Base):
    __tablename__ = 'gacha_pity_counter'

    player_id = Column(BigInteger, primary_key=True)
    pack_type = Column(String(50), primary_key=True)
    counter = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<GachaPityCounter(player_id={self.player_id}, pack_type='{self.pack_type}', counter={self.counter})>"
