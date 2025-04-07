from sqlalchemy import or_
from bot.entity.pkBattle import PkBattle

class PkBattleRepository:
    def __init__(self, session):
        self.session = session

    def createBattle(self, attacker_id: int, defender_id: int, attacker_card_id: int, defender_card_id: int, result: str, attacker_rank_change: int = 0) -> PkBattle:
        """
        Tạo bản ghi mới cho trận chiến (battle).
        :param attacker_id: ID của người tấn công.
        :param defender_id: ID của người bị tấn công.
        :param attacker_card_id: ID của thẻ chiến đấu của người tấn công.
        :param defender_card_id: ID của thẻ chiến đấu của người bị tấn công.
        :param result: Kết quả trận chiến ('win', 'loss', 'draw').
        :param attacker_rank_change: Thay đổi điểm rank của người tấn công.
        :return: Đối tượng PkBattle vừa được tạo.
        """
        battle = PkBattle(
            attacker_id=attacker_id,
            defender_id=defender_id,
            attacker_card_id=attacker_card_id,
            defender_card_id=defender_card_id,
            result=result,
            attacker_rank_change=attacker_rank_change
        )
        self.session.add(battle)
        self.session.commit()
        return battle

    def getBattleById(self, battle_id: int) -> PkBattle | None:
        """
        Lấy thông tin trận chiến theo battle_id.
        """
        return self.session.query(PkBattle).filter_by(battle_id=battle_id).first()

    def getBattlesForPlayer(self, player_id: int):
        """
        Lấy danh sách trận chiến mà người chơi tham gia (với tư cách là attacker hoặc defender).
        """
        return self.session.query(PkBattle).filter(
            or_(PkBattle.attacker_id == player_id, PkBattle.defender_id == player_id)
        ).all()
