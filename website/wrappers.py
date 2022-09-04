from functools import wraps

from flask import abort, redirect, url_for, request, jsonify
from flask_login import current_user
from services.web.core.logger import log, LogType


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (current_user.is_authenticated and (current_user.admin == 3)):
            abort(404)
        return f(*args, **kwargs)

    return decorated_function


def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401)
        return f(*args, **kwargs)

    return decorated_function()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.signin", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def log_result(f, log_level=6):
    def _decorate(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            log(f.__name__ + ": " + str(result), log_level, LogType.DEBUG)
            return result

        return decorated_function

    if f:
        return _decorate(f)

    return _decorate
