from bot.entity.challenge import Challenge

class ChallengeRepository:
    def __init__(self, session):
        self.session = session

    def createChallenge(self, challenge: Challenge) -> Challenge:
        """
        Tạo mới một bản ghi Challenge.
        """
        self.session.add(challenge)
        self.session.commit()
        return challenge

    def getChallengeById(self, challengeId: int) -> Challenge | None:
        """
        Lấy một bản ghi Challenge theo challengeId.
        """
        return self.session.query(Challenge).filter_by(id=challengeId).first()

    def getAllChallenges(self) -> list[Challenge]:
        """
        Lấy tất cả các bản ghi Challenge.
        """
        return self.session.query(Challenge).all()

    def updateChallenge(self, challenge: Challenge) -> Challenge:
        """
        Cập nhật thông tin của một bản ghi Challenge sau khi đã thay đổi thuộc tính.
        """
        self.session.commit()
        return challenge

    def deleteChallenge(self, challenge: Challenge):
        """
        Xóa một bản ghi Challenge khỏi cơ sở dữ liệu.
        """
        self.session.delete(challenge)
        self.session.commit()
