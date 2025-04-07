from sqlalchemy import Column, Integer, BigInteger, Enum, TIMESTAMP, text, ForeignKey
from bot.config.database import Base

class PkBattle(Base):
    __tablename__ = 'pk_battles'
    
    battle_id = Column(Integer, primary_key=True, autoincrement=True)
    attacker_id = Column(BigInteger, ForeignKey('players.player_id'), nullable=False)
    defender_id = Column(BigInteger, ForeignKey('players.player_id'), nullable=False)
    attacker_card_id = Column(Integer, ForeignKey('player_cards.id'), nullable=False)
    defender_card_id = Column(Integer, ForeignKey('player_cards.id'), nullable=False)
    result = Column(Enum('win', 'loss', 'draw', name='pk_battle_result_enum'), nullable=False)
    attacker_rank_change = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    
    def __repr__(self):
        return (f"<PkBattle(battle_id={self.battle_id}, attacker_id={self.attacker_id}, "
                f"defender_id={self.defender_id}, result={self.result}, "
                f"attacker_rank_change={self.attacker_rank_change})>")
