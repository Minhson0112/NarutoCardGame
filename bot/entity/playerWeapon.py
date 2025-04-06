from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from bot.config.database import Base

class PlayerWeapon(Base):
    __tablename__ = 'player_weapons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(BigInteger, ForeignKey('players.player_id'), nullable=False)
    weapon_key = Column(String(50), ForeignKey('weapon_templates.weapon_key'), nullable=False)
    level = Column(Integer, nullable=False, default=1)
    quantity = Column(Integer, nullable=False, default=1)
    equipped_card_id = Column(Integer, ForeignKey('player_cards.id'), nullable=True)
    slot_number = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    # Relationship: mỗi PlayerWeapon có một WeaponTemplate liên kết
    template = relationship("WeaponTemplate", backref="playerWeapons", lazy='joined')

    def __repr__(self):
        return (f"<PlayerWeapon(id={self.id}, player_id={self.player_id}, "
                f"weapon_key='{self.weapon_key}', level={self.level}, quantity={self.quantity}, "
                f"slot_number={self.slot_number})>")
