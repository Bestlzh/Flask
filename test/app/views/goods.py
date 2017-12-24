from flask import Blueprint, request, render_template, flash, url_for, redirect, current_app
from flask_login import login_user, login_required, current_user, logout_user

from app.extensions import db
from app.models import Goods
goods = Blueprint('goods',__name__)


# 商品列表
@goods.route('/goodslist',methods = ['GET','POST'])
def goodslist():
    goods = Goods.query.order_by().all()
    return render_template('goods/goodslist.html',goods = goods)


# 商品详情,增加浏览次数
@goods.route('/goodinfo/<int:gid>')
def goodinfo(gid):
    good = Goods.query.filter_by(id = gid).first()
    good.viemcount = good.viemcount + 1
    db.session.add(good)
    db.session.commit()
    return render_template('goods/goodinfo.html',good = good)



# 添加,取消收藏
@goods.route('/docollect/<int:gid>', methods=['GET', 'POST'])
@login_required
def docollect(gid):
    g = Goods.query.filter_by(id=gid).first()
    if g in current_user.goods:
        current_user.goods.remove(g)
        flash('取消收藏成功')
        db.session.add(current_user)
        db.session.commit()

        usercollect = current_user.goods
        return render_template('goods/showcollect.html', usercollect=usercollect)

    else:
        current_user.goods.append(g)
        db.session.add(current_user)
        db.session.commit()
        flash('收藏成功')
        return '收藏成功'



# 展示我的收藏
@goods.route('/showcollect/',methods =['GET','POST'])
@login_required
def showcollect():
    usercollect = current_user.goods
    return render_template('goods/showcollect.html',usercollect=usercollect)
