from flask import Blueprint, render_template

web = Blueprint('web', __name__)  # 实例化一个Blueprint 类对象创建蓝图
# 两个必要参数'web'蓝图名字;'__name__'蓝图所在的模块或者包，一般为'__name__'变量


@web.app_errorhandler(404) #蓝图的装饰器，接受状态码404
def not_found(e):
    return render_template('404.html'), 404


from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish



