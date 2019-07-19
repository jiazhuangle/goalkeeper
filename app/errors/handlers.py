from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as er


def needs_json():
    return request.accecpt_mimetypes['application/json'] >= \
           request.accept_mimetypes['text/html']

@bp.app_errorhandler(404)
def not_found_error(error):
    if needs_json():
        return er(404)
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if needs_json():
        return er(500)
    return render_template('errors/500.html'), 500