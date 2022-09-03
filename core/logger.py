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
"""logs for the server"""
import datetime
import logging
from services.web.core.color import color_text, OKBLUE, OKGREEN, WARNING, FAIL
from services.web.website.config import GlobalConfig


class LogType:
    DEBUG = logging.debug
    INFO = logging.info
    SUCCESS = logging.debug
    WARNING = logging.warning
    ERROR = logging.error


def log_message(message: str, now):
    def logger():
        print(color_text("[" + now + "] ", OKBLUE) + message)

    return logger


def log(message: str, log_level=1, logger=LogType.INFO) -> None:
    """This function logs using the python logging function and also prints out the message"""
    now = str(datetime.datetime.now())
    logger("[" + now + "] " + message)
    if int(log_level) <= int(GlobalConfig.log_level):
        if (logger == LogType.INFO) or (logger == LogType.DEBUG):
            to_log = log_message(message, now)
        elif logger == LogType.SUCCESS:
            to_log = log_message(color_text(message, OKGREEN), now)
        elif logger == LogType.WARNING:
            to_log = log_message(color_text(message, WARNING), now)
        elif logger == LogType.ERROR:
            to_log = log_message(color_text(message, FAIL), now)
        else:
            to_log = log_message(message, now)
        to_log()
