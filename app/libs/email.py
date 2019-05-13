from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message

#定义了异步函数
def send_async_email(app, msg):
    with app.app_context(): #入栈
        try:
            mail.send(msg)
        except Exception as e:
            pass

def send_mail(to, suject, template, **kwargs):
    # msg = Message('测试邮件', sender='824949896@qq.com', body='Test',  #body为正文内容 recipients要发送的邮箱地址
    #               recipients=['user@qq.com'])
    app = current_app._get_current_object() #详解见12-11
    msg = Message('[鱼书]' + '' + suject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])  #主线程中定义异步线程
    thr.start()
    # mail.send(msg)

