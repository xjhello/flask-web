from flask import render_template

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web


__author__ = '七月'


@web.route('/')
def index():
    recent_gifts = Gift.recent() #遍历礼物列表生成图书模型展示
    books = [BookViewModel(gift.book) for gift in recent_gifts] #book方法通过isbn返回图书
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    pass
