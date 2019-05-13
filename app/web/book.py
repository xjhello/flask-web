from flask import request, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search/')
def search():
    # q = request.args['q']
    # page = request.args['page']
    form = SearchForm(request.args)  # 验证层实例化，传入的参数是q和page 直接request.args
    books = BookCollection()  # view_model用于处理剪切从api获得的原始数据

    if form.validate():  # 判断是否通过验证
        q = form.q.data  # 取值q
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)  # 用于判断是isbn还是key
        yushu_book = YuShuBook()  # 调用豆瓣api

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)  # 调用isbn搜索方式
            # result = YuShuBook.search_by_isbn(q)
            # result = BookViewModel.package_single(result, q)
        else:
            yushu_book.search_by_keyword(q, page)  # 调用关键字搜索方式
            # result = YuShuBook.search_by_keyword(q, page)
            # result = BookViewModel.package_collection(result, q)
        books.fill(yushu_book, q)  # 将数据传入view_model进行数据剪切
        # return jsonify(books)
    else:
        flash('搜索的关键字不符合要求')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False  # 设置默认值不在礼物清单也不再礼物清单
    has_in_wishes = False

    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()  # 从数据库中查询
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes_model = TradeInfo(trade_wishes)  # 将数据填入到模型
    trade_gifts_model = TradeInfo(trade_gifts)
    return render_template('book_detail.html', book=book, has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model)


@web.route('/test')
def test():
    r = {
        'name': '徐健',
        'age': 18
    }
    return render_template('test.html', data=r)


@web.route('/hello')
def hello():
    return 'hello!!!!1'
