from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import StringField,PasswordField,BooleanField, DateTimeField,validators, FloatField, SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError

from app.extensions import photos
from app.models import User

# 注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(6,12,message='长度6-12之间')])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,18,message='密码长度6-18位')])
    confirm = PasswordField('确认密码',validators=[EqualTo('password',message='密码不一致.')])
    email = StringField('邮箱', validators=[DataRequired(), Email(message='格式不正确')])
    submit = SubmitField('注册')



    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            return ValidationError('该用户名被占用.')

    def validate_email(self,field):
        if User.query.filter_by(email = field.data).first():
            return ValidationError('一个邮箱只能注册一个用户.')

#         用户登录
class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

    def validate_username(self,field):
        if not User.query.filter_by(username=field.data).first():
            return ValidationError('用户名不存在')


#密码修改表单
class ModifypasswdForm(FlaskForm):
    oldpasswd = PasswordField('旧密码',validators=[DataRequired()])
    password = PasswordField('新密码', validators=[DataRequired(), Length(6, 18, message='密码长度6-18位')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='密码不一致.')])
    submit = SubmitField('修改')


# 头像上传表单
class IconForm(FlaskForm):
    icon = FileField('头像',validators=[FileRequired('请选择文件'),
                                      FileAllowed(photos,'只能是图片')])
    submit=SubmitField('上传')


# 修改邮箱表单
class ChangeEmail(FlaskForm):
    password = StringField('密码',validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email(message='格式不正确')])
    submit = SubmitField('修改')


#     找回密码
class FindPasswordForm(FlaskForm):
    email = StringField('请填写您注册账户的邮箱', validators=[DataRequired(), Email(message='格式不正确')])
    submit = SubmitField('找回')
# 重置密码
class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 18, message='密码长度6-18位')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='密码不一致.')])
    submit = SubmitField('修改')