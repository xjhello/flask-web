from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.libs.email import send_mail
from app.models.base import db
from app.models.user import User
from . import web


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)  # 得到request请求发送的数据进行验证
    if request.method == 'POST' and form.validate():
        with db.auto_commit():  #
            user = User()  # 实例化user模型
            user.set_attrs(form.data)  # 把传过来的参数设置给模型，这里使用了form表单的数据，发现form对象和user对象
            db.session.add(user)       # （加入到数据库）有相同的属性，所以使用hasattr函数判断form是否是user拥有的属性然后赋值！
        #   db.session.commit()  # 提交，这里把提交操作封装到了重构的db类
        return redirect(url_for('web.login'))  # redirect函数页面跳转
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()  # 查询用户
        if user and user.check_password(form.password.data):  # 检查密码
            login_user(user, remember=True)  # 使用登录插件，把用户登录票据(id号)写入到cookie，(remember表示持续的)
            # login_user规定在模型内部定义函数返回可以标识身份信息的数据即get_id(固定形式)
            next = request.args.get('next')  # next记录跳转页面地址，request.args.get获取？之后的next的参数(之前的页面)
            if not next or not next.startswith('/'):  # 如果next不存在跳转到首页，next.startswith('/')防止重定向攻击
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误', category='login_error')
    return render_template('auth/login.html', form=form)


@web.route('/logout')
def logout():
    logout_user()  # 登录插件的退出
    return redirect(url_for('web.index'))


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            send_mail(form.email.data, '重置你的密码',
                      'email/reset_password.html', user=user,
                      token=user.generate_token())
            flash('一封邮件已发送到邮箱' + account_email + '，请及时查收')
            # return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html')


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('web.index'))
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        result = User.reset_password(token, form.password1.data)
        if result:
            flash('你的密码已更新,请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            return redirect(url_for('web.index'))
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass
