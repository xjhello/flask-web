from flask import current_app, flash, redirect, url_for, render_template

from app.models.base import db
from app.models.gift import Gift
from app.setting import BEANS_UPLOAD_ONE_BOOK
from app.view_models.gift import MyGifts
from . import web
from flask_login import login_required, current_user


@web.route('/my/gifts')
@login_required  # 插件修饰器，用户必须登录才能访问(要想使用还需要为插件编写个函数在user中的get_id)
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gift(uid)  # 接受所有礼物的集合清单
    isbn_list = [gift.isbn for gift in gifts_of_mine]  # 取出每个礼物中的isbn编号组成一个列表
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)
    # return "MY gifts"
    return render_template('my_gifts.html', gifts=view_model.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # 既不在赠送清单，也不在心愿清单才能添加
        #     try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id  # current_user就是user实例化的模型
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']  # 鱼豆
            db.session.add(gift)  # 保存礼物数据到数据库
        #   db.session.commit()
        # except Exception as e:
        #     db.session.rollback()  #数据库事务回滚
        #     raise e
    else:
        flash("'这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
