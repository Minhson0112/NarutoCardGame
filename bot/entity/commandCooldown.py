# bot/entity/commandCooldown.py
from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from bot.config.database import Base

class CommandCooldown(Base):
    __tablename__ = 'command_cooldowns'

    player_id = Column(BigInteger, ForeignKey('players.player_id', ondelete='CASCADE'), primary_key=True)
    last_buy_multicard = Column(TIMESTAMP,nullable=True,server_default=text('NULL'))


    player = relationship("Player", back_populates="command_cooldown")

    def __repr__(self):
        return (f"<CommandCooldown(player_id={self.player_id}, "
                f"last_buy_multicard={self.last_buy_multicard})>")
