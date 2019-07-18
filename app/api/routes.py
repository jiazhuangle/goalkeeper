import base64
from flask import jsonify
from app.api import bp
from app.api.errors import bad_request
from app.models import UserData

@bp.route('/token/<user_info>',methods=['GET'])
def get_token(user_info):
    if not user_info:
        return bad_request('invalid request')
    userInfo = eval(str(base64.b64decode(user_info),'utf-8'))
    if 'username' not in userInfo or 'password' not in userInfo:
        return bad_request('invalid request')

    username = userInfo['username']
    password= userInfo['password']

    user = UserData.query.filter_by(username=username).first()
    if user is None:
        return bad_request('invalid request')
    if user.check_password(password):
        return jsonify(user.get_token())
    else:
        return bad_request('invalid request')


bp.route('/user/<token>', methods=['GET'])
def get_user(token):
    user = UserData.check_token(token) if token else None
    if user is not None:
        return jsonify(user.to_dict())
    else:
        return bad_request('invalid request')