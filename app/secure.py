#此文件包含数据库密码账号等机密数据，生产环境相关的配置，此文件不应该上传到git
DEBUG = True
# SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:7insummer@139.196.96.50:3307/fisher'
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@localhost:3306/fisher'
SECRET_KEY = '\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJ:U\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'

# Email 配置
MAIL_SERVER = 'smtp.126.com' #指定邮件服务地址
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TSL = True
MAIL_USERNAME = 'xujianzq886@126.com'
MAIL_PASSWORD = 'xujianzq123'
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SENDER = '鱼书 <hello@yushu.im>'