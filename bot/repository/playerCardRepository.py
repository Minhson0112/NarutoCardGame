from bot.entity.playerCards import PlayerCard
from bot.entity.cardTemplate import CardTemplate  

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

    def incrementQuantity(self, playerId: int, cardKey: str, level: int = 1, increment: int = 1):
        """
        Thêm thẻ vào kho của người chơi. 
        """
        # 1) Tìm bản ghi hiện có với cùng cardKey + level TRONG KHO (INVENTORY)
        existing_card = (
            self.session.query(PlayerCard)
            .filter_by(player_id=playerId, card_key=cardKey, level=level, status='INVENTORY')
            .first()
        )

        if existing_card:
            # Nếu đã có, chỉ tăng quantity
            existing_card.quantity += increment
            # Đảm bảo trạng thái là INVENTORY để hiện ra kho đồ
            existing_card.status = 'INVENTORY'
        else:
            # Tạo mới bản ghi
            new_card = PlayerCard(
                player_id=playerId,
                card_key=cardKey,
                level=level,
                quantity=increment,
                locked=False,
                status='INVENTORY'
            )
            self.session.add(new_card)

        self.session.commit()


    def getByCardNameAndPlayerId(self, player_id: int, card_name: str):
        """
        Lấy danh sách các thẻ của người chơi có tên khớp với card_name.

        :param player_id: ID của người chơi
        :param card_name: Tên thẻ cần tìm
        :return: Danh sách các đối tượng PlayerCard thỏa điều kiện
        """
        return (
            self.session.query(PlayerCard)
            .join(CardTemplate, PlayerCard.card_key == CardTemplate.card_key)
            .filter(
                PlayerCard.player_id == player_id,
                CardTemplate.name == card_name
            )
            .all()
        )
    
    def getEquippedCardsByPlayerId(self, playerId: int):
        """
        Lấy danh sách các thẻ của người chơi đang được cài đặt (equipped).
        """
        return self.session.query(PlayerCard).filter(
            PlayerCard.player_id == playerId,
            PlayerCard.equipped == True
        ).all()
    
    def deleteCard(self, card):
        """Xóa bản ghi thẻ khỏi session."""
        self.session.delete(card)
        
    def getByPlayerIdAndCardKey(self, playerId: int, cardKey: str):
        """
        Lấy tất cả các thẻ của một người chơi theo cùng card_key.
        Thường dùng để:
        - kiểm tra các level khác nhau của cùng 1 thẻ
        - tính tổng số phôi (level 1)
        - tìm level cao nhất của thẻ đó

        :param playerId: ID người chơi
        :param cardKey:  card_key trong bảng card_templates
        :return: Danh sách PlayerCard thỏa điều kiện
        """
        return (
            self.session.query(PlayerCard)
            .filter(
                PlayerCard.player_id == playerId,
                PlayerCard.card_key == cardKey
            )
            .all()
        )

    def apply_rank_reset_level_penalty(self):
        """
        Áp dụng trừ cấp cho toàn bộ thẻ theo rule reset rank:
            <10:   không trừ
            10–19: -5 (nhưng không bao giờ < 10)
            20–29: -10
            30–39: -15
            >=40:  -20

        Đảm bảo: KHÔNG thẻ nào sau reset bị tụt xuống dưới level 10 vì bị trừ cấp.
        (Các thẻ vốn <10 vẫn giữ nguyên, không đụng tới.)
        """
        q = self.session.query(PlayerCard)

        # 10–14: nếu trừ 5 sẽ <10 → clamp về 10
        q.filter(
            PlayerCard.level >= 10,
            PlayerCard.level < 15
        ).update(
            {PlayerCard.level: 10},
            synchronize_session=False
        )

        # 15–19: trừ 5 vẫn >=10 → OK
        q.filter(
            PlayerCard.level >= 15,
            PlayerCard.level < 20
        ).update(
            {PlayerCard.level: PlayerCard.level - 5},
            synchronize_session=False
        )

        # 20–29: -10 → 10–19
        q.filter(
            PlayerCard.level >= 20,
            PlayerCard.level < 30
        ).update(
            {PlayerCard.level: PlayerCard.level - 10},
            synchronize_session=False
        )

        # 30–39: -15 → 15–24
        q.filter(
            PlayerCard.level >= 30,
            PlayerCard.level < 40
        ).update(
            {PlayerCard.level: PlayerCard.level - 15},
            synchronize_session=False
        )

        # >=40: -20 → >=20
        q.filter(
            PlayerCard.level >= 40
        ).update(
            {PlayerCard.level: PlayerCard.level - 20},
            synchronize_session=False
        )