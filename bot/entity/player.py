from sqlalchemy import Column, BigInteger, String, Integer, TIMESTAMP, text
from bot.config.database import Base

class Player(Base):
    __tablename__ = 'players'
    
    player_id = Column(BigInteger, primary_key=True)
    username = Column(String(100))
    coin_balance = Column(Integer, nullable=False, default=0)
    rank_points = Column(Integer, nullable=False, default=0)
    highest_rank_points = Column(Integer, nullable=False, default=0)
    winning_streak = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP, 
        server_default=text("CURRENT_TIMESTAMP"), 
        server_onupdate=text("CURRENT_TIMESTAMP")
    )

    def __repr__(self):
        return f"<Player(player_id={self.player_id}, username='{self.username}')>"
