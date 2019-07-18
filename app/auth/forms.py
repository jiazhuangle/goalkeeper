from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')



class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('请求重置')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '密码确认', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('重置')