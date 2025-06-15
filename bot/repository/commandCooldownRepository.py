from datetime import datetime, timezone
from sqlalchemy.orm import Session
from bot.entity.commandCooldown import CommandCooldown

class CommandCooldownRepository:
    """
    Repository for command_cooldowns table. Provides methods to get and update cooldown timestamps.
    """
    def __init__(self, session: Session):
        self.session = session

    def find_by_player(self, player_id: int) -> CommandCooldown | None:
        """
        Lấy bản ghi CommandCooldown cho player_id, hoặc None nếu chưa có.
        """
        return self.session.get(CommandCooldown, player_id)

    def get_last_buy_multicard(self, player_id: int) -> datetime | None:
        """
        Trả về timestamp lần cuối dùng lệnh buymulticard, hoặc None nếu chưa từng.
        """
        record = self.find_by_player(player_id)
        return record.last_buy_multicard if record else None

    def set_last_buy_multicard(self, player_id: int, timestamp: datetime | None = None) -> None:
        """
        Cập nhật hoặc tạo mới last_buy_multicard cho player_id.
        Nếu timestamp không được cung cấp, sẽ dùng thời điểm hiện tại UTC.
        """
        ts = timestamp or datetime.now(timezone.utc)
        record = self.find_by_player(player_id)
        if record:
            record.last_buy_multicard = ts
        else:
            record = CommandCooldown(
                player_id=player_id,
                last_buy_multicard=ts
            )
            self.session.add(record)
        self.session.commit()