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

from flask import abort, Blueprint, request, jsonify, render_template
from flask_login import login_user, current_user
from services.web.core.data import check_auth
from services.web.core.logger import log, LogType
from services.web.website.models import database
from services.web.website.models.lesson_models import Lesson
from services.web.website.models.user_model import User

api = Blueprint("api", __name__)


@api.route("/api/")
def api_home():
    return render_template("api.html")


@api.route("/api/l/<lesson_id>/")
def access_lesson_api(lesson_id):
    lesson_requested = Lesson.query.filter_by(lesson_id=lesson_id).first()
    if lesson_requested is None:
        abort(404)
    return jsonify(
        title=lesson_requested.title,
        subtitle=lesson_requested.subtitle,
        image=lesson_requested.image,
        content=lesson_requested.body,
        goes_to=lesson_requested.goes_to,
    )


@api.route("/api/el/<lesson_id>/")
def edit_lesson(lesson_id):
    if current_user.is_authenticated and (current_user.admin == 3):
        try:
            lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()
            lesson.lesson_id = request.args.get("lesson_id", lesson.lesson_id, type=str)
            lesson.title = request.args.get("title", lesson.title, type=str)
            lesson.subtitle = request.args.get("subtitle", lesson.subtitle, type=str)
            lesson.image = request.args.get("image", lesson.image, type=str)
            lesson.body = request.args.get("body", lesson.body, type=str)
            lesson.goes_to = request.args.get("goes_to", lesson.goes_to, type=int)
            database.session.commit()
            return jsonify(status="s")
        except RuntimeError:
            return jsonify(status="f")
    else:
        abort(404)


@api.route("/api/validate-signup")
def signup_ajax():
    """Signup API"""
    username = request.args.get("username", "", type=str)
    email = request.args.get("email", "", type=str)
    if len(username) < 5:
        return jsonify(error="Your username needs to have more than 4 characters.")
    elif "@" not in email:
        return jsonify(error="Make sure your email is an email.")
    return jsonify(error="none")


@api.route("/api/signin/", methods=["POST"])
def signin_api():
    """Signin POST API"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = check_auth(username, password)
        if not user:
            return jsonify(result="f")
        else:
            login_user(user, remember=True)
            log(user.username + " successfully authenticated", 5, LogType.DEBUG)
            return jsonify(result="s")


@api.route("/api/ep/", methods=["POST"])
def edit_profile():
    """Edit profile"""
    if request.method == "POST":
        email = request.form["email"]
        about = request.form["about"]
        age = request.form["age"]
        user = User.query.filter_by(id=current_user.id).first()
        user.email = email
        user.about = about
        if age != "":
            user.age = int(age)
        database.session.commit()
        return jsonify(status="s")


@api.route("/api/notifications/")
def notifications():
    if current_user.is_authenticated:
        notification_string = current_user.notifications
        if notification_string == "":
            return jsonify({})
        notification_list = notification_string.split(",")

        return jsonify(notifications=notification_list)
    else:
        abort(401)
