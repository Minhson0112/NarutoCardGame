from datetime import date
from sqlalchemy.orm import Session
from bot.entity.dailyTask import DailyTask

class DailyTaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def getOrCreateDailyTask(self, playerId: int) -> DailyTask:
        """
        Lấy thông tin nhiệm vụ của người chơi theo playerId với ngày hiện tại (date.today()).
        Nếu chưa có bản ghi, tạo mới với ngày hiện tại.
        Nếu đã có nhưng ngày hiện tại khác với mission_date trong db, reset các bộ đếm về 0 và cập nhật mission_date.
        """
        currentDate = date.today()
        dailyTask = self.session.query(DailyTask).filter_by(player_id=playerId).first()
        if dailyTask is None:
            dailyTask = DailyTask(player_id=playerId, mission_date=currentDate)
            self.session.add(dailyTask)
            self.session.commit()
        elif dailyTask.mission_date != currentDate:
            dailyTask.mission_date = currentDate
            dailyTask.fight_win_count = 0
            dailyTask.fightwith_count = 0
            dailyTask.minigame_count = 0
            dailyTask.shop_buy_count = 0
            dailyTask.shop_sell_count = 0
            dailyTask.stage_clear_count = 0
            self.session.commit()
        return dailyTask

    def updateFightWin(self, playerId: int, count: int = 1) -> DailyTask:
        """
        Tăng số lần chiến thắng của lệnh fight.
        """
        dailyTask = self.getOrCreateDailyTask(playerId)
        dailyTask.fight_win_count += count
        self.session.commit()
        return dailyTask

    def updateFightwith(self, playerId: int, count: int = 1) -> DailyTask:
        """
        Tăng số lần sử dụng lệnh fightwith.
        """
        dailyTask = self.getOrCreateDailyTask(playerId)
        dailyTask.fightwith_count += count
        self.session.commit()
        return dailyTask

    def updateMinigame(self, playerId: int, count: int = 1) -> DailyTask:
        """
        Tăng số lần chơi minigame.
        """
        dailyTask = self.getOrCreateDailyTask(playerId)
        dailyTask.minigame_count += count
        self.session.commit()
        return dailyTask

    def updateShopBuy(self, playerId: int, count: int = 1) -> DailyTask:
        """
        Tăng số lần mua trong cửa hàng.
        """
        dailyTask = self.getOrCreateDailyTask(playerId)
        dailyTask.shop_buy_count += count
        self.session.commit()
        return dailyTask

    def updateShopSell(self, playerId: int, count: int = 1) -> DailyTask:
        """
        Tăng số lần bán trong cửa hàng.
        """
        dailyTask = self.getOrCreateDailyTask(playerId)
        dailyTask.shop_sell_count += count
        self.session.commit()
        return dailyTask

    def updateStageClear(self, playerId: int, count: int = 1) -> DailyTask:
        """
        Tăng số lần vượt ải.
        """
        dailyTask = self.getOrCreateDailyTask(playerId)
        dailyTask.stage_clear_count += count
        self.session.commit()
        return dailyTask

    def getDailyTaskInfo(self, playerId: int) -> DailyTask:
        """
        Trả về bản ghi nhiệm vụ của người chơi theo playerId với ngày hiện tại.
        Phương thức này sẽ tự động reset nếu ngày trong DB khác với ngày hiện tại.
        """
        return self.getOrCreateDailyTask(playerId)
