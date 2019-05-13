from sqlalchemy import Column, Integer, String
from app.models.base import db


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column('author', String(30), default='未名')
    binding = Column(String(20))  # 精装还是瓶装
    publisher = Column(String(50))  # 出版社
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))  # 出版日期
    isbn = Column(String(15), nullable=False, unique=True)  # unique设为不重复
    summary = Column(String(1000))
    image = Column(String(50))

    def sample(self):
        pass
