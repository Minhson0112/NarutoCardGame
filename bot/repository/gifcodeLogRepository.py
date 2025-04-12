from typing import List, Optional
from bot.entity.gifcodeLog import GifcodeLog

class GifcodeLogRepository:
    def __init__(self, session):
        self.session = session

    def createGifcodeLog(self, playerId: int, gifcodeId: int) -> GifcodeLog:
        """
        Tạo một bản ghi log mới khi người chơi sử dụng mã gifcode.
        """
        log = GifcodeLog(player_id=playerId, gifcode_id=gifcodeId)
        self.session.add(log)
        self.session.commit()
        return log

    def hasPlayerUsed(self, playerId: int, gifcodeId: int) -> bool:
        """
        Kiểm tra xem người chơi đã sử dụng mã gifcode với gifcodeId cho trước chưa.
        Trả về True nếu có ít nhất một bản ghi, ngược lại trả về False.
        """
        count = self.session.query(GifcodeLog).filter_by(player_id=playerId, gifcode_id=gifcodeId).count()
        return count > 0

    def getAllLogs(self) -> List[GifcodeLog]:
        """
        Lấy danh sách tất cả các bản ghi log của gifcode.
        """
        return self.session.query(GifcodeLog).all()
