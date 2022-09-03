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

from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from services.web.core.wrappers import login_required
from services.web.website import cache

main = Blueprint("main", __name__)


@main.route("/home", endpoint="index")
@main.route("/", endpoint="index")
def index():
    """Home page"""
    return render_template("main/home.jinja")


@main.route("/about", endpoint="about")
@cache.cached(timeout=604800)
def about():
    return render_template("main/about.jinja")


@main.route("/articles", endpoint="articles")
@cache.cached(timeout=10)
def articles():
    return render_template("main/articles.jinja")


class Project:
    """Project wrapper class"""

    def __init__(self, name, image, link):
        self.name = name
        self.image = image
        self.link = link


@main.route("/projects")
@login_required
def projects():
    return render_template("main/projects.jinja", projects=[], crowd_projects=[])


@main.route("/test-code", endpoint="redirect_test_code")
@main.route("/runcode", endpoint="redirect_test_code")
@main.route("/run-code-online", endpoint="redirect_test_code")
@main.route("/runcodeonline", endpoint="redirect_test_code")
@main.route("/testcode", endpoint="redirect_test_code")
@cache.cached(timeout=31536000)
def redirect_test_code():
    """Redirects to /run-code"""
    return redirect("/run-code")


@main.route("/run-code", endpoint="test_code")
@cache.cached(timeout=31536000)
def test_code():
    """/run-code run code list page"""
    return render_template("main/run_code.jinja")


@main.route("/packages")
def packages():
    """
    /packages
    """
    return render_template("main/packages.jinja")


@main.route("/account", endpoint="account")
@login_required
def account():
    """
    /account
    """
    return render_template("main/account.jinja", user=current_user)


@main.route("/release-notes")
def release_notes():
    return render_template("main/release-notes.jinja")
