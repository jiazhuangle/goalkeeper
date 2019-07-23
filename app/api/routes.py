import base64
from flask import jsonify,g
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from app.models import UserData


@bp.route('/user', methods=['GET'])
@token_auth.login_required
def get_user():
    return jsonify(g.current_user.to_dict())