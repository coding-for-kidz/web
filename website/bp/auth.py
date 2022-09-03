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

import os
from secrets import compare_digest

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from services.web.core.spam_detector import spam_detector
from services.web.website import login_manager, mail

# from flask_dance.contrib.google import google
from services.web.website.config import Config
from services.web.website.models import database
from services.web.website.models.user_model import User

# from website import csrf
from services.web.core.logger import log

login_manager.login_view = "home"

auth = Blueprint("auth", __name__)


# TODO: ADD URL
# TODO: ADD OTHER PROVIDERS
# https://flask-dance.readthedocs.io/en/latest/quickstart.html
# def auth_google():
#     """
#     Google auth
#     :return:
#     """
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     resp = google.get("/oauth2/v1/userinfo")
#     assert resp.ok, resp.text
#     return resp.json()


@auth.route("/register", methods=["GET", "POST"], endpoint="signup")
@auth.route("/sign_up", methods=["GET", "POST"], endpoint="signup")
@auth.route("/sign-up", methods=["GET", "POST"], endpoint="signup")
@auth.route("/signup", methods=["GET", "POST"], endpoint="signup")
def signup():
    """signup page"""
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        error = ""
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]
        about = request.form["about"]
        email = request.form["email"]
        age = request.form["age"]
        try:
            profile_picture = request.files["file"]
        except Exception:
            profile_picture = None
        if username == "":
            error = "You did not enter any username."
        elif len(username) < 4:
            error = "Your username must contain at least 4 letters."
        elif " " in username:
            error = "Your username cannot contain any spaces."
        elif not compare_digest(confirm_password, password):
            error = "Your passwords do not match."
        elif compare_digest(password, ""):
            error = "You did not enter a password"
        elif len(password) < 6:
            error = "Your password must contain at least 6 letters."
        elif bool(User.query.filter_by(username=username).first()):
            error = "The username is already taken."
        elif spam_detector(username):
            error = "Rude words are not allowed."
        else:
            for user in User.query.all():
                if user.username.lower() == username.lower():
                    error = "The username is already taken."
        if error == "":
            user = User()
            user.username = username
            user.about = about
            user.age = age
            user.password = generate_password_hash(password, method="pbkdf2:sha512")
            user.admin = 0
            user.email = email
            if profile_picture is not None:
                filename = secure_filename(username + "-profile-picture")
                profile_picture.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                user.image = "/uploads/" + username + "-profile-picture"
            else:
                user.image = "/uploads/default.jpg"
            database.session.add(user)
            database.session.commit()
            login_user(user, remember=True)
            flash("You have successfully signed up", "success")
            log(user.username + " signed up", 2)
            return redirect(url_for("/"))
        else:
            return render_template(
                "auth/signup.jinja",
                error=error,
                username="",
                password="",
                confirm="",
                about="",
            )
    else:
        return render_template(
            "auth/signup.jinja",
            error="",
            username="",
            password="",
            confirm="",
            about="",
        )


@auth.route("/sign_in/", endpoint="redirect_signin")
@auth.route("/sign-in/", endpoint="redirect_signin")
@auth.route("/login/", endpoint="redirect_signin")
@auth.route("/log-in/", endpoint="redirect_signin")
@auth.route("/logon/", endpoint="redirect_signin")
@auth.route("/log-on/", endpoint="redirect_signin")
def redirect_signin():
    """Redirects to /signin"""
    return redirect("/signin", 301)


@auth.route("/signin/", endpoint="signin")
def signin():
    """The sign-in page"""
    if current_user.is_authenticated:
        return redirect("/", 307)
    return render_template("auth/signin.jinja", error="", text="", password="")


@auth.route("/signout/", endpoint="redirect_logout")
@auth.route("/sign_out/", endpoint="redirect_logout")
@auth.route("/sign-out/", endpoint="redirect_logout")
@auth.route("/log_out/", endpoint="redirect_logout")
@auth.route("/log-out/", endpoint="redirect_logout")
def redirect_logout():
    """Redirects to log out"""
    return redirect("/logout", 301)


@auth.route("/logout/", endpoint="logout")
def logout():
    """Logs out user"""
    if current_user.is_authenticated:
        logout_user()
    return redirect("/", 307)


@auth.route("/forgot-password/", methods=["GET", "POST"])
def forgot_password():
    """Forgot password page"""
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username)
        if user.email is None:
            error = "There is no email associated with your account."
        elif user.email == "":
            error = "You did not enter an email."
        elif user is None:
            error = "There is no account with that username."
        else:
            msg = Message(
                "Password Reset for Coding for Kidz",
                sender="passwordreset@coding-for-kidz.herokuapp.com",
                recipients=[user.email],
            )
            msg.body = (
                "Dear "
                + user.username
                + ",\nYou can reset your password at this link. This link will expire "
                "in 24 hours. If you did not request a password reset you can safely"
                "ignore the email.\nThanks,\nThe Coding for Kidz team "
            )
            msg.html = (
                "Dear "
                + user.username
                + ",<br><br>You can reset your password here. This link will expire in"
                " 24 hours. If you did not request a password reset you can safely"
                " ignore the email.<br><br>Thanks,<br><br>The Coding for Kidz Team"
            )
            mail.send(msg)
            flash("You will have received an email with a link to reset your passcode.")
            return redirect("/")
        return render_template("auth/forgotpassword.jinja", error=error)

    else:
        return render_template("auth/forgotpassword.jinja", error=error)
