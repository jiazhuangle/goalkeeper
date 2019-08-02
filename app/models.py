from werkzeug.security import generate_password_hash, check_password_hash
from time import time
from datetime import datetime, timedelta
from flask import current_app
import jwt,os,base64
from flask_login import UserMixin
from app import db, login


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    title = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

"""
status:
1: 正常状态
0：已删除状态
"""
class UserData(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    title = db.Column(db.String(64))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    status = db.Column(db.String(32))

    def __repr__(self):
        return '<UserData {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=36000):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            pass
        else:
            self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
            self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)

        return self.token

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'title':self.title,
            'status':self.status,
        }
        return data


    @staticmethod
    def check_token(token):
        user = UserData.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user