# 添加扩展
# 导入相关类库
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES
from flask_uploads import configure_uploads,patch_request_class


# 创建相关对象
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
migrate = Migrate(db=db)
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)


# 完成相关初始化
def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    migrate.init_app(app)
    # 登录
    login_manager.init_app(app)
    # 未登录提示信息
    login_manager.login_message = '请您登录后访问'
    # 指定登录的视图函数
    login_manager.login_view='user.login'
    # 设置session级别
    # none:禁用保护
    # 'basic'基本保护级别,默认值
    # 'strong'最严格的保护
    login_manager.session_protection = 'strong'

    configure_uploads(app,photos)
    # 指定上传文件的大小,None,采用配置的值
    patch_request_class(app,size=None)