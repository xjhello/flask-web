from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  #
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):  # 继承UserMixin继承其中的属性用于登录
    # __tablename__ = 'user' 改变表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    _password = Column('password', String(100))
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property  # 把方法设置为属性，读取类属性
    def password(self):
        return self._password

    @password.setter  # 写入属性
    def password(self, raw):  # raw为原始明文密码
        self._password = generate_password_hash(raw)  # 明文密码加密

    def check_password(self, raw):  # 检查明文密码
        if not self._password:
            return False
        return check_password_hash(self._password, raw)  # 先加密明文密码再对比数据库，成功返回True

    #   login_user中存在许多类属性(就包括get_id)，一个一个写太麻烦，让User模型继承UserMixin就行了
    #     def get_id(self): #格式固定的，返回的是代表用户身份的标识，是login_user插件规定的必须要有的
    #          return self.id1

    def can_save_to_list(self, isbn):  # 验证添加礼物赠送清单的isbn编号是否符合
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,  # 不允许一个用户同时赠送多本相同图书
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,  # 一个用户不可能同时成为赠送者和索要者
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):  # 生成id加密后的token。expiration过期时间秒
        s = Serializer(current_app.config['SECRET_KEY'], expiration)  # Serializer序列化器，SECRET_KEY独一无二的字符串
        return s.dumps({'id': self.id}).decode('utf-8')  # 写入序列化器，接受字典 decode转化为字符串

    @staticmethod  # 更新密码
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))  # 转化token得到id
        except:
            return False
        user = User.query.get(data.get('id'))
        if user is None:
            return False
        user.password = new_password
        db.session.commit()
        return True


# 不是模型的函数，是模块的函数
@login_manager.user_loader  # 装饰器标识让Flask_login 调用
def get_id(uid):  # 通过id号返回用户模型
    return User.query.get(int(uid))
