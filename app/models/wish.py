from sqlalchemy.orm import relationship
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, SmallInteger, desc, func
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13),)
    launched = Column(Boolean, default=False)
    # status = Column(SmallInteger) #删除状态

    #根据用户的uid查询当前用户的所有的礼物
    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod #根据传入的一组isbn到Gift表中检索相应的礼物。并计算某个礼物总数
    def get_gifts_counts(cls, isbn_list):
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

        # 根据isbn取图书
    @property  # 属性描述符
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

from app.models.gift import Gift