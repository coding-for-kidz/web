# Copyright 2021 Coding for Kidz Project
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

from flask import (
    Blueprint,
    redirect,
    Response,
    render_template,
    session,
    send_from_directory,
)
from flask_login import current_user
from werkzeug.exceptions import abort

from services.web.core import path
from services.web.website import cache
from services.web.website.models import database

util = Blueprint("util", __name__)


@util.route("/privacy")
def privacy():
    return render_template("util/privacypolicy.html")


@util.route("/tos")
def terms_of_service():
    """Notice that it is a html document, not a template"""
    return render_template("util/terms_of_service.html")


@util.route("/robots.txt", endpoint="robots")
@cache.cached(timeout=31536000)
def robots():
    pwd = str(path.cfk_dir() / "services" / "web" / "website" / "static")
    resp = send_from_directory(pwd, "robots.txt")
    return resp


@util.route("/favicon.ico")
def favicon():
    pwd = str(path.cfk_dir() / "services" / "web" / "website" / "static")
    resp = send_from_directory(pwd, "favicon.ico")
    return resp


@util.route("/refresh", endpoint="refresh")
@cache.cached(timeout=31536000)
def refresh() -> Response:
    return redirect("/", 301)


@util.route("/createall", endpoint="create_all")
@util.route("/create-all", endpoint="create_all")
@cache.cached(timeout=31536000)
def create_all() -> Response:
    """Creates all the db"""
    if current_user.is_authenticated and (current_user.admin == 3):
        database.create_all()
        return redirect("/admin-site/")
    else:
        abort(404)


@util.route("/debug-sentry")
@cache.cached(timeout=60400)
def trigger_error():
    """Triggers 0 division error"""
    if current_user.is_authenticated and (current_user.admin == 3):
        return 1 / 0
    else:
        abort(404)


@util.route("/offline")
@cache.cached(timeout=3600)
def offline():
    return render_template("offline.jinja")


@util.route("/os-css.css")
def os_css():
    css = ""
    if session["style"] == "apple":
        css = ".topnav { border-radius: 10px; }"
    elif session["style"] == "sun valley":
        css = ".topnav { border-radius: 5px; }"
    response = Response(css)
    response.content_type = "text/css"
    return response
