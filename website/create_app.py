"""Creates the app object"""
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
import logging
import sys

import flask.cli
import sentry_sdk
from flask import request, session, render_template
from htmlmin import minify

from services.web.core.http_parse import OperatingSystem, UserAgent
from services.web.core.logger import log, LogType
from services.web.website.cfk_flask import CFKFlask
from services.web.website.config import (
    DevConfig,
    ProdConfig,
    TestConfig,
    DockerConfig,
    GlobalConfig,
    BuiltInConfig,
)

with open("main.log", "w") as main_log:
    main_log.write("")
    main_log.close()

logging.basicConfig(filename="main.log", encoding="utf-8", level=logging.DEBUG)
werkzeug_log = logging.getLogger("werkzeug")
werkzeug_log.setLevel(logging.ERROR)


def init():
    log(
        "Starting server version "
        + GlobalConfig.version
        + "-"
        + GlobalConfig.release_status
        + " "
        + GlobalConfig.codename
        + " | Python v"
        + str(sys.version_info[0])
        + "."
        + str(sys.version_info[1])
        + "."
        + str(sys.version_info[2])
        + " | Flask v"
        + flask.__version__,
        1,
        LogType.SUCCESS,
    )


def _select_jinja_autoescape(filename):
    """
    Returns `True` if autoescaping should be active for the given template name.
    """
    if filename is None:
        return False
    return filename.endswith((".html", ".htm", ".xml", ".xhtml", ".jinja", ".jinja2"))


def create_app(
        config_file="", development=False, testing=False, docker=False, log_level=1
) -> CFKFlask:
    """Creates the app
    @param config_file: the config file
    @param development: for development
    @param testing: only set to true when testing with pytest
    @param docker: whether the app is containerized or not
    @param log_level: 0 is quiet and 5 is the most verbose
    """
    GlobalConfig.development = development
    GlobalConfig.log_level = log_level
    GlobalConfig.docker = docker
    if config_file != "":
        BuiltInConfig(config_file)
    init()

    log("Creating app", 2)
    app = CFKFlask(__name__)

    if development:
        log("Using Development Config", 3)
        app.config.from_object(DevConfig)
    elif testing:
        log("Using Testing Config", 3)
        app.config.from_object(TestConfig)
    elif docker:
        log("Using Docker Config", 3)
        GlobalConfig.redis = True
        app.config.from_object(DockerConfig)
    else:
        log("Defaulting to Production Config", 3)
        app.config.from_object(ProdConfig)

    app.jinja_env.autoescape = _select_jinja_autoescape
    log("All config finished", 2)
    # dashboard.config.init_from(file='config.cfg')
    # logging
    if (not testing) and (not development) and GlobalConfig.sentry:
        try:
            from services.web.website.website_secrets import SENTRY_SDK_DSN
            from sentry_sdk.integrations.flask import FlaskIntegration

            sentry_sdk.init(
                dsn=SENTRY_SDK_DSN,
                integrations=[FlaskIntegration()],
                traces_sample_rate=0.1,
            )
            log("Sentry initialised", 2)
        except ImportError as e:
            log("Failed to import SENTRY_SDK_DSN " + str(e))
        except Exception as e:
            log("Sentry initialisation failed: {}".format(e), 2, LogType.ERROR)
            log("Sentry initialisation failed", 1, LogType.ERROR)
    else:
        log("Skipping sentry initialisation", 2, LogType.WARNING)

    from services.web.website.services import init_services

    init_services(app)
    log("All services initialised")

    # importing models
    from services.web.website.models import database

    database.init_app(app)
    log("Models registered", 2)
    # blueprint import and registration
    from services.web.website.bp import register_blueprints

    register_blueprints(app)
    log("Blueprints registered", 2)

    log("Utility Views and Errors initialized", 3)
    log("Finished", logger=LogType.SUCCESS)
    from services.web.website import register_mimetypes

    register_mimetypes.register_mimetypes()

    @app.before_request
    def before():
        user_agent = UserAgent(request.headers.get("User-Agent"))
        operating_system = user_agent.get_os()
        if (operating_system == OperatingSystem.macOs) or (
            operating_system == OperatingSystem.ios
        ):
            session["style"] = "apple"
        elif (operating_system == OperatingSystem.Windows_NT) and (
            user_agent.get_os_version(
                str(request.headers.get("Sec-Ch-Ua-Platform-Version"))
            )
            == 11
        ):
            session["style"] = "sun valley"
        else:
            session["style"] = "default"
        log(
            "Request at "
            + request.url
            + " by "
            + str(request.remote_addr)
            + "\nBrowser: "
            + user_agent.get_browser().capitalize()
            + " v"
            + user_agent.get_browser_version()
            + "\nOS: "
            + str(operating_system)[16 : len(str(operating_system))]  # noqa E203
            + " v"
            + user_agent.get_os_version(
                str(request.headers.get("Sec-Ch-Ua-Platform-Version"))
            ),
            4,
            LogType.DEBUG,
        )

    @app.after_request
    def after(response):
        response.headers["accept-ch"] = "Sec-Ch-Ua-Platform,Sec-Ch-Ua-Platform-Version"
        if str(response.content_type) == "text/html; charset=utf-8":
            response.set_data(
                minify(response.get_data(as_text=True), remove_comments=True)
            )
        return response

    @app.errorhandler(400)
    def error_400(e):
        """Error 400"""
        return render_template("errors/client_error_400.jinja")

    @app.errorhandler(401)
    def error_401(e):
        """Error 401"""
        import random

        exercises = ["push-ups", "sit-ups", "jumping jacks", "toe taps", "push-ups"]
        number = random.randint(0, len(exercises))
        return (
            render_template("errors/access_denied.jinja", exercise=exercises[number]),
            401,
        )

    @app.errorhandler(404)
    def error_404(e):
        """Error 404"""
        return render_template("errors/not_found.jinja"), 404

    @app.errorhandler(405)
    def error_405(e):
        """Error 405"""
        return render_template("errors/client_error_405.jinja"), 405

    @app.errorhandler(413)
    def error_413(e):
        """Error 413"""
        return (
            'The file is too large<br><a href=" / ">Return to the home page </a>.',
            413,
        )

    @app.errorhandler(418)
    def error_418(e):
        """Error 418"""
        return render_template("errors/teapot.jinja"), 418

    @app.errorhandler(500)
    def error_500(e):
        """Error 500"""
        from sentry_sdk import last_event_id

        return (
            render_template(
                "errors/server_error.jinja", sentry_event_id=last_event_id(), error=e
            ),
            500,
        )

    return app
