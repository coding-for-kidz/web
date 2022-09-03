from functools import wraps

from flask import abort, redirect, url_for, request
from flask_login import current_user


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
        if (current_user is None) or (not current_user.is_authenticated):
            abort(401)
        return f(*args, **kwargs)

    return decorated_function()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.signin", next=request.url))
        return f(*args, **kwargs)

    return decorated_function
