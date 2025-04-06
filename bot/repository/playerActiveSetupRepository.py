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
