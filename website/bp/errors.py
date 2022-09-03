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

from flask import render_template, abort, flash, redirect, request, Blueprint
from flask_login import current_user

from services.web.website.models import database, NotFoundError

errors = Blueprint("errors", __name__)


@errors.route("/error", endpoint="test_error_handler_base")
@errors.route("/error-test")
def test_error_handler_base():
    return render_template("errors/status_codes.jinja")


@errors.route("/error-test/<int:e>/")
def test_error_handler(e: int):
    abort(e)


@errors.route("/teapot")
def teapot():
    abort(418)


@errors.route(
    "/page_not_found_error",
    methods=("GET", "POST"),
    endpoint="report_page_not_found_error_redirect",
)
@errors.route(
    "/page_not_found_error",
    methods=("GET", "POST"),
    endpoint="report_page_not_found_error_redirect",
)
@errors.route(
    "/pagenotfounderror",
    methods=("GET", "POST"),
    endpoint="report_page_not_found_error_redirect",
)
def report_page_not_found_error_redirect():
    """
    Redirects to /page-not-found-error
    """
    return redirect("/page-not-found-error")


@errors.route(
    "/page-not-found-error",
    methods=("GET", "POST"),
    endpoint="report_page_not_found_error",
)
def report_page_not_found_error():
    if request.method == "POST":
        url = request.form["url"]
        not_found_error = NotFoundError()
        not_found_error.url = url
        if not current_user.is_authenticated:
            not_found_error.reporter = current_user.username
        else:
            not_found_error.reporter = "N/A"
        database.session.add(not_found_error)
        database.commit()
        flash("Your report has been submitted", "info")
    else:
        return render_template("errors/report_error/page_not_found_error.jinja")
