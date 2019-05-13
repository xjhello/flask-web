from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer


class SQLAlchemy(_SQLAlchemy):  # SQLAlchemy的子类 重构commit方法使其自动提交
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):  # 重构filter_by方法
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)  # 替换


class Base(db.Model):
    __abstract__ = True  # 设置为基类，不创建Base表
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):  # 装入创建时间
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs):  # 接受attrs为字典
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id':  # hasattr函数用于判断当前对象是否包含key属性。id不需要添加
                setattr(self, key, value)  # 动态复赋值setattr函数，用于设置属性值，该属性必须存在。

    @property  # 时间转换
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
