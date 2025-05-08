from sqlalchemy import Column, Integer, BigInteger, Boolean, TIMESTAMP, text, ForeignKey, String
from sqlalchemy.orm import relationship
from bot.config.database import Base

class PlayerCard(Base):
    __tablename__ = 'player_cards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(BigInteger, ForeignKey('players.player_id'), nullable=False)
    card_key = Column(String(50), ForeignKey('card_templates.card_key'), nullable=False)
    level = Column(Integer, nullable=False, default=1)
    quantity = Column(Integer, nullable=False, default=1)
    equipped = Column(Boolean, nullable=False, default=False)
    locked = Column(Boolean, nullable=False, default=False, server_default=text('0'))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    # Relationship: mỗi PlayerCard có một CardTemplate liên kết
    template = relationship("CardTemplate", backref="playerCards", lazy='joined')

    def __repr__(self):
        return (
            f"<PlayerCard(id={self.id}, player_id={self.player_id}, "
            f"card_key='{self.card_key}', level={self.level}, "
            f"quantity={self.quantity}, equipped={self.equipped}, locked={self.locked})>"
        )
