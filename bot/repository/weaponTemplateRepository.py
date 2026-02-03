import random
from typing import Optional, List
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

    def getByName(self, name: str) -> Optional[WeaponTemplate]:
            """
            Lấy WeaponTemplate theo name (dùng cho /showweapon).
            """
            return self.session.query(WeaponTemplate).filter_by(name=name).first()

    def searchNamesForAutocomplete(self, typed: str, limit: int = 25) -> List[str]:
        """
        Trả về danh sách tên vũ khí phục vụ autocomplete.
        Ưu tiên match prefix trước, nếu chưa đủ thì bổ sung match contains.
        """
        typed = (typed or "").strip()
        if not typed:
            return []

        prefix_rows = (
            self.session
            .query(WeaponTemplate.name)
            .filter(WeaponTemplate.name.like(f"{typed}%"))
            .order_by(WeaponTemplate.name.asc())
            .limit(limit)
            .all()
        )
        names = [r[0] for r in prefix_rows]

        if len(names) < limit:
            remaining = limit - len(names)
            contains_rows = (
                self.session
                .query(WeaponTemplate.name)
                .filter(WeaponTemplate.name.like(f"%{typed}%"))
                .order_by(WeaponTemplate.name.asc())
                .limit(remaining)
                .all()
            )
            for r in contains_rows:
                if r[0] not in names:
                    names.append(r[0])
                    if len(names) >= limit:
                        break

        return names