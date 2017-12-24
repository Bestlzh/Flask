from app.extensions import db

class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer,primary_key=True)
    goodname = db.Column(db.String)
    goodprice = db.Column(db.Float)
    icon = db.Column(db.String(128))
    content = db.Column(db.Text)
    viemcount = db.Column(db.Integer,default=0)

# 多对多的关联表创建
collect = db.Table(
    'collect_table',
    db.Column('good_id', db.Integer, db.ForeignKey('goods.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
)