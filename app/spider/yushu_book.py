from app.libs.httpr import HTTP
from flask import current_app


class YuShuBook:
    # per_page = 15
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):  # cls是classmethod的关键字
        url = self.isbn_url.format(isbn)  # 格式化，把isbn加到URL后面
        result = HTTP.get(url)  # 发送http请求，得到json，序列化为dict
        self.__fill_sifle(result)

    def __fill_sifle(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'],
                                      self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']  # current_app指代当前app核心对象

    @property  # 返回第一个图书对象
    def first(self):
        return self.books[0] if self.total >= 1 else None
