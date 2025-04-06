from bot.entity.PlayerActiveSetup import PlayerActiveSetup

class PlayerActiveSetupRepository:
    def __init__(self, session):
        self.session = session

    def createEmptySetup(self, player_id: int):
        setup = PlayerActiveSetup(player_id=player_id)
        self.session.add(setup)
        self.session.commit()

    def getByPlayerId(self, player_id: int) -> PlayerActiveSetup | None:
        return self.session.query(PlayerActiveSetup).filter_by(player_id=player_id).first()

    def updateActiveCard(self, player_id: int, card_id: int):
        """
        Cập nhật active_card_id cho active setup của người chơi.
        """
        active_setup = self.getByPlayerId(player_id)
        if active_setup is None:
            raise ValueError(f"Không tìm thấy active setup cho người chơi với ID {player_id}")
        active_setup.active_card_id = card_id
        self.session.commit()
        return active_setup
    
    def updateActiveWeapon(self, playerId: int, weaponId: int):
        """
        Cập nhật trường weaponSlot1 trong active setup của người chơi.
        """
        activeSetup = self.getByPlayerId(playerId)
        if activeSetup is None:
            raise ValueError(f"Không tìm thấy active setup cho người chơi với ID {playerId}")
        activeSetup.weapon_slot1 = weaponId
        self.session.commit()
        return activeSetup