'''
    创建应用程序，并注册相关蓝图
'''
from flask import Flask
from flask_mail import Mail
from app.models.book import db
from flask_login import LoginManager

login_manager = LoginManager()  # 登录插件
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')  # 导入载入配置文件 参数为模块路径
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    db.create_all(app=app)  # 调用db
    login_manager.init_app(app)  # 登录插件初始化
    login_manager.login_view = "web.login"  # 当访问无权限的URL时返回到这里的页面，让插件知道登录界面是哪个
    login_manager.login_message = '请先登录或者注册'  # 文字提醒

    mail.init_app(app)  # 注册插件
    # with app.app_context():
    #     db.create_all()
    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)   # 把蓝图注册到Flask核心对象app
