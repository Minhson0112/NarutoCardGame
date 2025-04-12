from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP, text, BigInteger
from bot.config.database import Base

class GifcodeLog(Base):
    __tablename__ = 'gifcode_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(BigInteger, ForeignKey("players.player_id"), nullable=False)
    gifcode_id = Column(Integer, ForeignKey("gifcode.id"), nullable=False)
    rewarded_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    
    def __repr__(self):
        return f"<GifcodeLog(id={self.id}, playerId={self.playerId}, gifcodeId={self.gifcodeId})>"