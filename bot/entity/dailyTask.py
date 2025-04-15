from sqlalchemy import Column, BigInteger, Date, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from bot.config.database import Base

class DailyTask(Base):
    __tablename__ = 'daily_tasks'
    
    # Sử dụng player_id làm khóa chính, liên kết với bảng players
    player_id = Column(BigInteger, ForeignKey("players.player_id"), primary_key=True)
    
    # Lưu trữ ngày hiện hành của nhiệm vụ (sẽ được reset và cập nhật mỗi ngày)
    mission_date = Column(Date, nullable=False)
    
    # Các cột đếm cho từng hành động của nhiệm vụ
    fight_win_count = Column(Integer, nullable=False, default=0)
    fightwith_count = Column(Integer, nullable=False, default=0)
    minigame_count = Column(Integer, nullable=False, default=0)
    shop_buy_count = Column(Integer, nullable=False, default=0)
    shop_sell_count = Column(Integer, nullable=False, default=0)
    stage_clear_count = Column(Integer, nullable=False, default=0)
    
    # Các cột lưu trạng thái "đã nhận thưởng" cho từng nhiệm vụ (true nếu đã claim thưởng)
    fight_win_claimed = Column(Boolean, nullable=False, default=False)
    fightwith_claimed = Column(Boolean, nullable=False, default=False)
    minigame_claimed = Column(Boolean, nullable=False, default=False)
    shop_buy_claimed = Column(Boolean, nullable=False, default=False)
    shop_sell_claimed = Column(Boolean, nullable=False, default=False)
    stage_clear_claimed = Column(Boolean, nullable=False, default=False)
    
    # Optional: Liên kết với entity Player
    player = relationship("Player", backref="daily_task", uselist=False)
    
    def __repr__(self):
        return (
            f"<DailyTask(player_id={self.player_id}, mission_date={self.mission_date}, "
            f"fight_win_count={self.fight_win_count}, fightwith_count={self.fightwith_count}, "
            f"minigame_count={self.minigame_count}, shop_buy_count={self.shop_buy_count}, "
            f"shop_sell_count={self.shop_sell_count}, stage_clear_count={self.stage_clear_count}, "
            f"fight_win_claimed={self.fight_win_claimed}, fightwith_claimed={self.fightwith_claimed}, "
            f"minigame_claimed={self.minigame_claimed}, shop_buy_claimed={self.shop_buy_claimed}, "
            f"shop_sell_claimed={self.shop_sell_claimed}, stage_clear_claimed={self.stage_clear_claimed})>"
        )
