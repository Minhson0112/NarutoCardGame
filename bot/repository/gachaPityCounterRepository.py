from bot.entity.gachaPityCounter import GachaPityCounter

class GachaPityCounterRepository:
    def __init__(self, session):
        self.session = session

    def getCount(self, playerId: int, packType: str) -> int:
        entry = self.session.query(GachaPityCounter).filter_by(player_id=playerId, pack_type=packType).first()
        return entry.counter if entry else 0

    def incrementCounter(self, playerId: int, packType: str, increment: int = 1):
        entry = self.session.query(GachaPityCounter).filter_by(player_id=playerId, pack_type=packType).first()
        if entry:
            entry.counter += increment
        else:
            entry = GachaPityCounter(player_id=playerId, pack_type=packType, counter=increment)
            self.session.add(entry)
        self.session.commit()

    def resetCounter(self, playerId: int, packType: str):
        entry = self.session.query(GachaPityCounter).filter_by(player_id=playerId, pack_type=packType).first()
        if entry:
            entry.counter = 0
            self.session.commit()

    def initializeCounter(self, playerId: int, packType: str):
        entry = self.session.query(GachaPityCounter).filter_by(player_id=playerId, pack_type=packType).first()
        if not entry:
            entry = GachaPityCounter(player_id=playerId, pack_type=packType, counter=0)
            self.session.add(entry)
            self.session.commit()