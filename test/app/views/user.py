import os

from PIL import Image
from flask import Blueprint, request, render_template, flash, url_for, redirect, current_app
from flask_login import login_user, login_required, current_user, logout_user

from app.extensions import db
from app.forms import RegisterForm, ResetPasswordForm,LoginForm, FindPasswordForm,ModifypasswdForm, IconForm,ChangeEmail
from app.models import User
from app.email import send_mail
from app.extensions import photos
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
user = Blueprint('user', __name__)


@user.route('/register/', methods=['GET', "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)

        # user = User(username = form.username.data,
        #             password = form.password.data,
        #             email = form.email.data)

        db.session.add(u)
        db.session.commit()
        token = u.generate_activate_token()
        send_mail(form.email.data, '账户激活', 'email/activate', token=token, username=u.username)
        flash('注册成功,查看邮件点击完成激活操作!')
        return redirect(url_for('main.index'))

    return render_template('user/register.html', form=form)


@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('账户激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败!')
        return redirect(url_for('main.index'))


@user.route('/login/', methods=['GET', "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            flash('无效用户名')
        elif u.verify_password(form.password.data):
            login_user(u, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效密码')
    return render_template('user/login.html', form=form)


@user.route('/logout/')
# 保护路由
@login_required
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('main.index'))


# 信息查看
@user.route('/profile/')
def profile():
    return render_template('user/profile.html')


# 修改密码
@user.route('/modifypasswd/', methods=['GET', "POST"])
@login_required
def modifypasswd():
    form = ModifypasswdForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpasswd.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('修改成功')
            return redirect(url_for('main.index'))
        else:
            flash('原密码错误.')
    return render_template('user/modifypasswd.html', form=form)

#重置密码
@user.route('/resetpassword/<token>',methods = ['GET','POST'])
def resetpassword(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        u = User.query.get(data.get('id'))
        u.password = form.password.data
        db.session.add(u)
        flash('密码重置成功')
        return redirect(url_for('user.login'))

    else:
        if User.check_activate_token(token):
            flash('验证成功,请重置密码')

        else:
            flash('操作失败!')
            return redirect(url_for('main.index'))
    return render_template('user/resetpassword.html',form = form)

# 找回密码
@user.route('/find_password/',methods = ['GET',"POST"])
def find_password():
    form = FindPasswordForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        token = u.generate_activate_token()

        send_mail(form.email.data, '密码找回', 'email/findpassword', token=token, username=u.username)
        flash('发送至您的邮箱,请查看邮件找回密码.')
    return render_template('user/find_password.html',form = form)


# 修改邮箱
@user.route('/change_email/',methods = ['GET',"POST"])
@login_required
def change_email():
    form =ChangeEmail()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.email = form.email.data
            current_user.confirmed = False
            db.session.add(current_user)
            db.session.commit()
            token = current_user.generate_activate_token()
            send_mail(form.email.data, '账户激活', 'email/activate', token=token, username=current_user.username)
            flash('邮箱更改成功,查看邮件点击完成激活操作!')

            return redirect(url_for('main.index'))


    return render_template('user/change_email.html',form = form)

# 头像修改
@user.route('/change_icon/', methods=['GET', 'POST'])
def change_icon():
    form = IconForm()
    if form.validate_on_submit():
        # 获取后缀
        # 生成随机的文件名
        suffix = os.path.splitext(form.icon.data.filename)[1]
        name = rand_str() + suffix
        photos.save(form.icon.data, name=name)
        # 缩略图
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], name)
        img = Image.open(pathname)
        img.thumbnail((64, 64))
        img.save(pathname)
        # 删除旧头像
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        # 数据库
        current_user.icon = name
        db.session.add(current_user)
        flash('头像已修改')
    return render_template('user/change_icon.html', form=form)


# 生成字符串
def rand_str(length=32):
    import random
    base_str = 'fsnskskjfnsjkfbsiubfwufbqwerqtrqiryqotpdlkasncn159841658146541616895o'
    return ''.join(random.choice(base_str) for i in range(length))
