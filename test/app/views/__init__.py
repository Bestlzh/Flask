
from .main import main
from .user import user
from .goods import goods
# 蓝本配置
DEFAULT_BLUEPRINT = (

    (main,'/main'),
    (user,'/user'),
    (goods,'/goods')
)
def config_blueprint(app):

    for blue_print,url_prefix in DEFAULT_BLUEPRINT:

        app.register_blueprint(blue_print,url_prefix=url_prefix)


