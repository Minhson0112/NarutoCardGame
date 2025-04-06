import random
from bot.entity.weaponTemplate import WeaponTemplate

class WeaponTemplateRepository:
    def __init__(self, session):
        self.session = session

    def getByKey(self, weaponKey: str) -> WeaponTemplate:
        """
        Lấy WeaponTemplate theo weapon_key.
        """
        return self.session.query(WeaponTemplate).filter_by(weapon_key=weaponKey).first()

    def getAllByGrade(self, grade: str):
        """
        Lấy tất cả các WeaponTemplate có grade nhất định.
        """
        return self.session.query(WeaponTemplate).filter_by(grade=grade).all()

    def getRandomByGrade(self, grade: str) -> WeaponTemplate:
        """
        Trả về ngẫu nhiên một WeaponTemplate có grade được chỉ định.
        """
        templates = self.getAllByGrade(grade)
        if templates:
            return random.choice(templates)
        return None
