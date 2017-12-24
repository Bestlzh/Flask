# 配置的基类
import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config():

    SECRET_KEY ='123456'
    #代码改变时自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    # 取消代码改变时的追踪提示
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送
    MAIL_SERVER =os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_USERNAME =os.environ.get('MAIL_USERNAME') or'13116090713@163.com'
    MAIL_PASSWORD =os.environ.get('MAIL_PASSWORD') or'123456zlj'
    # 上传文件的大小，默认不限制
    MAX_CONTENT_LENGTH = 6 * 1024 *1024
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/upload')

    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(base_dir,'blog-dev.sqlite')

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')

class ProdutionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-pro.sqlite')
# 对外公开的配置字典
config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProdutionConfig,
    'default':DevelopmentConfig
}
