from bot.entity.player import Player

class PlayerRepository:
    def __init__(self, session):
        self.session = session

    def getById(self, player_id: int) -> Player | None:
        return self.session.query(Player).filter_by(player_id=player_id).first()

    def create(self, player: Player):
        self.session.add(player)
        self.session.commit()
