from app.extensions import db
from flask import current_app
from   app.extensions import login_manager
from flask_login import UserMixin
# 用户状态的使用需要实现几个回调函数,这个类做了实现
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, DateTime, Text, Float
from werkzeug.security import generate_password_hash, check_password_hash
# 生成token使用的类
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .goods import collect
from app.views import user


class User(UserMixin,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(40),unique=True)
    confirmed = db.Column(db.Boolean,default=False)
    icon = db.Column(db.String(128),default='default.jpg')

    goods = db.relationship(
        'Goods',  # 关联的模型类
        secondary=collect,
        backref='collectuser',
    )

    @property
    def password(self):
        raise ArithmeticError('密码不可读')


    # 设置密码,加密存储
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    # 密码校验
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    #生成账户激活的token
    def generate_activate_token(self,expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expires_in)
        # 将字典数据串行化,生成乱码
        return s.dumps({"id": self.id})

    # 账户激活
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data.get('id'))
        if user is None:
            return False
        if not user.confirmed:
            # 激活
            user.confirmed = True
            db.session.add(user)
        return True

# 登陆认证回调
@login_manager.user_loader
def loader_user(user_id):
    return  User.query.get(int(user_id))