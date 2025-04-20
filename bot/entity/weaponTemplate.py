from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, text, Enum, Float
from bot.config.database import Base

class WeaponTemplate(Base):
    __tablename__ = 'weapon_templates'

    weapon_key = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    grade = Column(Enum('Normal', 'Rare', 'Legendary', name='weapon_grade_enum'), nullable=False)

    # Các chỉ số bonus (nullable = không buff)
    bonus_health = Column(Integer, nullable=True)
    bonus_armor = Column(Integer, nullable=True)
    bonus_damage = Column(Integer, nullable=True)
    bonus_crit_rate = Column(Float, nullable=True)  # VD: 0.05 = +5% crit
    bonus_speed = Column(Float, nullable=True)      # VD: 0.1 = +10% né tránh
    bonus_chakra = Column(Integer, nullable=True)

    image_url = Column(Text)
    sell_price = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return f"<WeaponTemplate(weapon_key='{self.weapon_key}', name='{self.name}', grade='{self.grade}')>"
