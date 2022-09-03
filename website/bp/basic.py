"""Basic functions"""
#  Copyright 2021 Coding for Kidz Project
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from flask import Blueprint, render_template, send_from_directory
from flask_login import current_user
from werkzeug.exceptions import abort

from services.web.website import login_manager
from services.web.website.models.user_model import User

basic = Blueprint("basic", __name__)

login_manager.login_view = "home"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@basic.route("/uploads/<filename>/")
def uploaded_file(filename):
    return send_from_directory("/uploads", filename)


@basic.route("/user/<username>/")
def view_user_profile(username):
    user = User.query.filter_by(usermane=username).first()
    if user is not None:
        return render_template("user_profile.jinja", user=user)
    else:
        abort(404)


@basic.route("/changeprofile")
def change_profile():
    if current_user.is_authenticated:
        return render_template(
            "basic/change_profile.jinja",
            user=User.query.filter_by(user_id=current_user.id).first(),
        )
    else:
        abort(404)
