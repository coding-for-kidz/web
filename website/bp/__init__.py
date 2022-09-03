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

"""Imports the blueprints and has a register_blueprints() function that registers the blueprints"""
from services.web.website.bp.admin import register_admin_blueprints
from services.web.website.bp.api import api
from services.web.website.bp.auth import auth
from services.web.website.bp.basic import basic
from services.web.website.bp.pwa import pwa
from services.web.website.bp.errors import errors
from services.web.website.bp.experiments import register_experimental_blueprints
from services.web.website.bp.lesson import lesson
from services.web.website.bp.main import main
from services.web.website.bp.testcode import testcode
from services.web.website.bp.util import util


def register_blueprints(app):
    """Registers all the blueprints"""
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(basic)
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(lesson)
    app.register_blueprint(pwa)
    app.register_blueprint(testcode)
    app.register_blueprint(util)

    register_admin_blueprints(app)
    register_experimental_blueprints(app)
