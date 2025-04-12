from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP, text, BigInteger
from sqlalchemy.orm import relationship
from bot.config.database import Base

class Gifcode(Base):
    __tablename__ = 'gifcode'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    gif_code = Column(String(100), nullable=False)
    gif_name = Column(String(255), nullable=False)
    bonus_ryo = Column(Integer, default=None)
    card_key = Column(String(50), ForeignKey("card_templates.card_key"), default=None)
    weapon_key = Column(String(50), ForeignKey("weapon_templates.weapon_key"), default=None)
    expiration_date = Column(Date)

    cardTemplate = relationship("CardTemplate", lazy="joined")
    weaponTemplate = relationship("WeaponTemplate", lazy="joined")

    def __repr__(self):
        return f"<Gifcode(id={self.id}, gifCode='{self.gifCode}', gifName='{self.gifName}')>"
