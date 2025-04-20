from bot.entity.PlayerActiveSetup import PlayerActiveSetup

class PlayerActiveSetupRepository:
    def __init__(self, session):
        self.session = session

    def createEmptySetup(self, player_id: int) -> PlayerActiveSetup:
        """
        Tạo record mới với cả 3 slot thẻ và 3 slot vũ khí đều NULL.
        """
        setup = PlayerActiveSetup(player_id=player_id)
        self.session.add(setup)
        self.session.commit()
        return setup

    def getByPlayerId(self, player_id: int) -> PlayerActiveSetup | None:
        """
        Lấy PlayerActiveSetup theo player_id, hoặc None nếu chưa có.
        """
        return (
            self.session
            .query(PlayerActiveSetup)
            .filter_by(player_id=player_id)
            .first()
        )

    def updateCardSlot1(self, player_id: int, card1_id: int | None) -> PlayerActiveSetup:
        """
        Cập nhật card_slot1 (slot tướng 1).
        """
        setup = self.getByPlayerId(player_id)
        if setup is None:
            raise ValueError(f"Không tìm thấy setup cho player_id={player_id}")
        setup.card_slot1 = card1_id
        self.session.commit()
        return setup

    def updateCardSlot2(self, player_id: int, card2_id: int | None) -> PlayerActiveSetup:
        """
        Cập nhật card_slot2 (slot tướng 2).
        """
        setup = self.getByPlayerId(player_id)
        if setup is None:
            raise ValueError(f"Không tìm thấy setup cho player_id={player_id}")
        setup.card_slot2 = card2_id
        self.session.commit()
        return setup

    def updateCardSlot3(self, player_id: int, card3_id: int | None) -> PlayerActiveSetup:
        """
        Cập nhật card_slot3 (slot tướng 3).
        """
        setup = self.getByPlayerId(player_id)
        if setup is None:
            raise ValueError(f"Không tìm thấy setup cho player_id={player_id}")
        setup.card_slot3 = card3_id
        self.session.commit()
        return setup

    def updateWeaponSlot1(self, player_id: int, weapon1_id: int | None) -> PlayerActiveSetup:
        """
        Cập nhật weapon_slot1 (slot vũ khí 1).
        """
        setup = self.getByPlayerId(player_id)
        if setup is None:
            raise ValueError(f"Không tìm thấy setup cho player_id={player_id}")
        setup.weapon_slot1 = weapon1_id
        self.session.commit()
        return setup

    def updateWeaponSlot2(self, player_id: int, weapon2_id: int | None) -> PlayerActiveSetup:
        """
        Cập nhật weapon_slot2 (slot vũ khí 2).
        """
        setup = self.getByPlayerId(player_id)
        if setup is None:
            raise ValueError(f"Không tìm thấy setup cho player_id={player_id}")
        setup.weapon_slot2 = weapon2_id
        self.session.commit()
        return setup

    def updateWeaponSlot3(self, player_id: int, weapon3_id: int | None) -> PlayerActiveSetup:
        """
        Cập nhật weapon_slot3 (slot vũ khí 3).
        """
        setup = self.getByPlayerId(player_id)
        if setup is None:
            raise ValueError(f"Không tìm thấy setup cho player_id={player_id}")
        setup.weapon_slot3 = weapon3_id
        self.session.commit()
        return setup
