from sqlalchemy import Column, BigInteger, Integer, TIMESTAMP, text, ForeignKey
from bot.config.database import Base

class PlayerActiveSetup(Base):
    __tablename__ = 'player_active_setup'

    player_id = Column(BigInteger, primary_key=True)

    # 3 slot tướng
    card_slot1 = Column(Integer, ForeignKey('player_cards.id'), nullable=True)  # Tank
    card_slot2 = Column(Integer, ForeignKey('player_cards.id'), nullable=True)
    card_slot3 = Column(Integer, ForeignKey('player_cards.id'), nullable=True)

    # 3 slot vũ khí
    weapon_slot1 = Column(Integer, ForeignKey('player_weapons.id'), nullable=True)
    weapon_slot2 = Column(Integer, ForeignKey('player_weapons.id'), nullable=True)
    weapon_slot3 = Column(Integer, ForeignKey('player_weapons.id'), nullable=True)

    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
