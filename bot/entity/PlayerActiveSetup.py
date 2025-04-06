from sqlalchemy import Column, BigInteger, Integer, TIMESTAMP, text
from bot.config.database import Base

class PlayerActiveSetup(Base):
    __tablename__ = 'player_active_setup'

    player_id = Column(BigInteger, primary_key=True)
    active_card_id = Column(Integer, nullable=True, default=None)
    weapon_slot1 = Column(Integer, nullable=True)
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
