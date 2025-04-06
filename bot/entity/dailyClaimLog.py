from sqlalchemy import Column, BigInteger, Date
from bot.config.database import Base

class DailyClaimLog(Base):
    __tablename__ = 'daily_claim_log'

    player_id = Column(BigInteger, primary_key=True)
    claim_date = Column(Date, primary_key=True)
