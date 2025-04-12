from typing import Optional, List
from bot.entity.gifcode import Gifcode

class GifcodeRepository:
    def __init__(self, session):
        self.session = session

    def getByGifCode(self, gifCode: str) -> Optional[Gifcode]:
        """
        Lấy một bản ghi Gifcode theo gifCode.
        """
        return self.session.query(Gifcode).filter_by(gif_code=gifCode).first()

    def createGifcode(self, gifcode: Gifcode) -> Gifcode:
        """
        Thêm một bản ghi Gifcode mới vào cơ sở dữ liệu.
        """
        self.session.add(gifcode)
        self.session.commit()
        return gifcode

    def updateGifcode(self, gifcode: Gifcode) -> Gifcode:
        """
        Cập nhật thông tin của một bản ghi Gifcode.
        """
        self.session.commit()
        return gifcode

    def deleteGifcode(self, gifcode: Gifcode):
        """
        Xóa bản ghi Gifcode khỏi cơ sở dữ liệu.
        """
        self.session.delete(gifcode)
        self.session.commit()

    def getAllGifcodes(self) -> List[Gifcode]:
        """
        Lấy danh sách tất cả các bản ghi Gifcode.
        """
        return self.session.query(Gifcode).all()
