from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import UserData

class AddUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])
    name=StringField('姓名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    title = StringField('职位', validators=[DataRequired()])
    submit = SubmitField('添加')

    def validate_username(self, username):
        user = UserData.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名已被占用,请重新输入.')

    def validate_email(self, email):
        user = UserData.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱已被占用,请重新输入.')