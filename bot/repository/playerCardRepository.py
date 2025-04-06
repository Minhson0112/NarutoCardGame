from bot.entity.playerCards import PlayerCard

class PlayerCardRepository:
    def __init__(self, session):
        self.session = session

    def getById(self, cardId: int) -> PlayerCard:
        """
        Lấy một bản ghi player card theo id.
        """
        return self.session.query(PlayerCard).filter_by(id=cardId).first()

    def getByPlayerId(self, playerId: int):
        """
        Lấy danh sách tất cả các thẻ của một người chơi.
        """
        return self.session.query(PlayerCard).filter_by(player_id=playerId).all()

    def getByPlayerAndCardKey(self, playerId: int, cardKey: str) -> PlayerCard:
        """
        Lấy bản ghi của người chơi theo card_key. Dùng để kiểm tra xem người chơi đã có thẻ này hay chưa.
        """
        return self.session.query(PlayerCard).filter_by(player_id=playerId, card_key=cardKey).first()

    def create(self, playerCard: PlayerCard):
        """
        Thêm một bản ghi mới vào bảng player_cards.
        """
        self.session.add(playerCard)
        self.session.commit()

    def update(self, playerCard: PlayerCard):
        """
        Cập nhật thông tin của bản ghi player card. Giả sử các trường đã được thay đổi.
        """
        self.session.commit()

    def incrementQuantity(self, playerId: int, cardKey: str, increment: int = 1):
        """
        Nếu người chơi đã có thẻ với cardKey, tăng số lượng của nó lên.
        Nếu chưa có, tạo bản ghi mới với số lượng là increment.
        """
        playerCard = self.getByPlayerAndCardKey(playerId, cardKey)
        if playerCard:
            playerCard.quantity += increment
        else:
            playerCard = PlayerCard(player_id=playerId, card_key=cardKey, quantity=increment)
            self.session.add(playerCard)
        self.session.commit()
