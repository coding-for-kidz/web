"""The module has the Config classes"""
import configparser

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
import datetime
import os

try:
    from services.shared.config import SharedConfig, SharedProdConfig, SharedDevConfig
except ImportError:

    class SharedConfig(object):
        """Base config"""

        CACHE_TYPE = "flask_caching.backends.SimpleCache"
        CACHE_DEFAULT_TIMEOUT = 300
        # sets the cookie settings
        SESSION_COOKIE_SECURE = True
        SESSION_COOKIE_HTTPONLY = True
        SESSION_COOKIE_SAMESITE = "Strict"
        SQLALCHEMY_TRACK_MODIFICATIONS = False  # Necessary

    class SharedDevConfig(SharedConfig):
        SQLALCHEMY_TRACK_MODIFICATIONS = True
        TEMPLATES_AUTO_RELOAD = True


    class SharedProdConfig(SharedConfig):
        """Production config"""

        debug = False
        DEBUG_TB_INTERCEPT_REDIRECTS = True
        TEMPLATES_AUTO_RELOAD = False

from services.secrets import (
    DATABASE_URI,
    SECRET_KEY,
    GOOGLE_OAUTH_CLIENT_ID,
    GOOGLE_OAUTH_CLIENT_SECRET,
)


class BuiltInConfig:
    def __init__(self, file):
        config = configparser.ConfigParser()
        config.read(file)
        self.cfk_config = config["cfk"]


class GlobalConfig:
    development = False
    docker = False
    sentry = True
    redis = False
    redis_port = 6379
    version = "0.0.0"
    release_status = "alpha"
    codename = "Great Dane"
    data_inited = str(datetime.datetime.now())
    log_level = 1
    admin_site = True
    allow_signin = True
    compile_frontend_on_start = False
    color_text = True
    debug = True
    sentry_traces_sample_rate = 0.1
    os_style = True
    init_sentry = True
    init_redis = False
    init_mail = True


class Config(SharedConfig):
    """Base config"""

    # sets the folder locations
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/website/static"
    MEDIA_FOLDER = (
        f"{os.getenv('APP_FOLDER')}/website/media"  # Leave empty, uploads go here
    )

    root_path = "coding-for-kidz/website"

    UPLOAD_FOLDER = "/uploads"
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    SQLALCHEMY_DATABASE_URI = DATABASE_URI  # secrets

    SECRET_KEY = SECRET_KEY  # secrets

    GOOGLE_OAUTH_CLIENT_ID = GOOGLE_OAUTH_CLIENT_ID  # secrets
    GOOGLE_OAUTH_CLIENT_SECRET = GOOGLE_OAUTH_CLIENT_SECRET  # secrets


class DevConfig(Config, SharedDevConfig):
    pass


class ProdConfig(Config, SharedProdConfig):
    pass


class DockerConfig(ProdConfig):
    """Docker config. Different database"""

    db = "postgresql://codingforkidzuser:codingforkidziscoolthisisthepasscode@localhost:5432/codingforkidzdatabase"
    TEMPLATES_AUTO_RELOAD = False


class TestConfig(Config):
    """Testing config"""

    debug = False
    testing = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    TEMPLATES_AUTO_RELOAD = False
