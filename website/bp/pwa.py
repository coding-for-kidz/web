import os

from flask import Blueprint, send_from_directory

pwa = Blueprint("pwa", __name__)


@pwa.route("/manifest.webmanifest")
def manifest():
    pwd = os.path.dirname(os.path.realpath(__file__))
    pwd = pwd[0: len(pwd) - 3] + "/static"  # noqa E203
    resp = send_from_directory(pwd, "manifest.webmanifest")
    resp.headers["Service-Worker-Allowed"] = ""
    return resp


@pwa.route("/service-worker.js")
def service_worker():
    pwd = os.path.dirname(os.path.realpath(__file__))
    pwd = pwd[0: len(pwd) - 3] + "/static"  # noqa E203
    resp = send_from_directory(pwd, "service-worker.js")
    return resp
