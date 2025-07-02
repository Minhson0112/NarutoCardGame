from bot.entity.player import Player

class PlayerRepository:
    def __init__(self, session):
        self.session = session

    def getById(self, player_id: int) -> Player | None:
        return self.session.query(Player).filter_by(player_id=player_id).first()

    def create(self, player: Player):
        self.session.add(player)
        self.session.commit()

    def getTop10(self) -> list[Player]:
        """
        Lấy danh sách Top 10 người chơi theo điểm rank (giảm dần).
        """
        return (
            self.session.query(Player)
            .order_by(Player.rank_points.desc())
            .limit(10)
            .all()
        )

    def getPlayerRank(self, playerId: int) -> int | None:
        """
        Xác định thứ hạng của một người chơi dựa vào điểm rank.
        Cách tính: thứ hạng = số người chơi có điểm rank cao hơn người này + 1.
        Trả về None nếu người chơi không tồn tại.
        """
        player = self.getById(playerId)
        if not player:
            return None
        higherCount = self.session.query(Player).filter(Player.rank_points > player.rank_points).count()
        return higherCount + 1
    
    def incrementExp(self, player_id: int, amount: int = 1) -> int:
        """
        Cộng thêm `amount` vào exp của người chơi.
        Trả về exp mới.
        """
        player = self.getById(player_id)
        if not player:
            raise ValueError(f"Không tìm thấy player với id={player_id}")
        player.exp += amount
        self.session.commit()
        return player.exp
    
    def getExp(self, player_id: int) -> int | None:
        """
        Lấy exp hiện tại của người chơi, hoặc None nếu không tồn tại.
        """
        player = self.getById(player_id)
        return player.exp if player else None
    