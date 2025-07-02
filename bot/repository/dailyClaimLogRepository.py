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

    def getLastClaimDate(self, playerId: int) -> date | None:
        """Trả về ngày điểm danh gần nhất trước hôm nay, hoặc None nếu chưa từng."""
        last = (
            self.session.query(DailyClaimLog.claim_date)
            .filter_by(player_id=playerId)
            .order_by(DailyClaimLog.claim_date.desc())
            .first()
        )
        return last[0] if last else None