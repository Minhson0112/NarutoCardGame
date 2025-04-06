from bot.entity.playerWeapon import PlayerWeapon

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
        Nếu người chơi đã có vũ khí với weaponKey, tăng số lượng của nó lên.
        Nếu chưa có, tạo bản ghi mới với số lượng là increment.
        """
        playerWeapon = self.getByPlayerAndWeaponKey(playerId, weaponKey)
        if playerWeapon:
            playerWeapon.quantity += increment
        else:
            playerWeapon = PlayerWeapon(player_id=playerId, weapon_key=weaponKey, quantity=increment)
            self.session.add(playerWeapon)
        self.session.commit()
