from datetime import date
from bot.entity.dailyClaimLog import DailyClaimLog

class DailyClaimLogRepository:
    def __init__(self, session):
        self.session = session

    def hasClaimedToday(self, playerId: int) -> bool:
        today = date.today()
        return self.session.query(DailyClaimLog).filter_by(player_id=playerId, claim_date=today).first() is not None

    def markClaimed(self, playerId: int):
        today = date.today()
        log = DailyClaimLog(player_id=playerId, claim_date=today)
        self.session.add(log)
        self.session.commit()
