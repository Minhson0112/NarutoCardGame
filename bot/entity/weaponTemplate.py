from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, text, Enum
from bot.config.database import Base

class WeaponTemplate(Base):
    __tablename__ = 'weapon_templates'

    weapon_key = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    grade = Column(Enum('Normal', 'Rare', 'Legendary', name='weapon_grade_enum'), nullable=False)
    bonus_power = Column(Integer)
    image_url = Column(Text)
    sell_price = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return f"<WeaponTemplate(weapon_key='{self.weapon_key}', name='{self.name}', grade='{self.grade}')>"
