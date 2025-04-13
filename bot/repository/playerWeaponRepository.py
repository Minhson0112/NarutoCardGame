from bot.entity.playerWeapon import PlayerWeapon
from bot.entity.weaponTemplate import WeaponTemplate

class PlayerWeaponRepository:
    def __init__(self, session):
        self.session = session

    def getById(self, weaponId: int) -> PlayerWeapon:
        """
        Lấy một bản ghi player weapon theo id.
        """
        return self.session.query(PlayerWeapon).filter_by(id=weaponId).first()

    def getByPlayerId(self, playerId: int):
        """
        Lấy danh sách tất cả các vũ khí của một người chơi.
        """
        return self.session.query(PlayerWeapon).filter_by(player_id=playerId).all()

    def getByPlayerAndWeaponKey(self, playerId: int, weaponKey: str) -> PlayerWeapon:
        """
        Lấy bản ghi của người chơi theo weapon_key.
        Dùng để kiểm tra xem người chơi đã có vũ khí này hay chưa.
        """
        return self.session.query(PlayerWeapon).filter_by(player_id=playerId, weapon_key=weaponKey).first()

    def create(self, playerWeapon: PlayerWeapon):
        """
        Thêm một bản ghi mới vào bảng player_weapons.
        """
        self.session.add(playerWeapon)
        self.session.commit()

    def update(self, playerWeapon: PlayerWeapon):
        """
        Cập nhật thông tin của bản ghi player weapon.
        """
        self.session.commit()

    def incrementQuantity(self, playerId: int, weaponKey: str, increment: int = 1):
        """
        Nếu người chơi đã có vũ khí với weaponKey ở cấp 1, tăng số lượng của nó lên.
        Nếu chưa có, tạo bản ghi mới với level = 1 và số lượng là increment.
        """
        # Tìm bản ghi PlayerWeapon với level == 1
        playerWeapon = self.session.query(PlayerWeapon).filter_by(
            player_id=playerId,
            weapon_key=weaponKey,
            level=1
        ).first()
        
        if playerWeapon:
            playerWeapon.quantity += increment
        else:
            playerWeapon = PlayerWeapon(
                player_id=playerId,
                weapon_key=weaponKey,
                level=1,
                quantity=increment
            )
            self.session.add(playerWeapon)
        
        self.session.commit()

    def getByWeaponNameAndPlayerId(self, playerId: int, weaponName: str):
        """
        Lấy danh sách các vũ khí của người chơi có tên khớp với weaponName.
        
        :param playerId: ID của người chơi
        :param weaponName: Tên vũ khí cần tìm
        :return: Danh sách các đối tượng PlayerWeapon thỏa điều kiện
        """
        return (
            self.session.query(PlayerWeapon)
            .join(WeaponTemplate, PlayerWeapon.weapon_key == WeaponTemplate.weapon_key)
            .filter(
                PlayerWeapon.player_id == playerId,
                WeaponTemplate.name == weaponName  # So sánh tên vũ khí trong template
            )
            .all()
    )

    def getEquippedWeaponsByPlayerId(self, playerId: int):
        """
        Lấy danh sách các vũ khí của người chơi đang được cài đặt (equipped).
        :param playerId: ID của người chơi
        :return: Danh sách các đối tượng PlayerWeapon với equipped=True
        """
        return self.session.query(PlayerWeapon).filter(
            PlayerWeapon.player_id == playerId,
            PlayerWeapon.equipped == True
        ).all()
    
    def deleteWeapon(self, weapon):
        self.session.delete(weapon)
