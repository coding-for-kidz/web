from flask import render_template, Blueprint

settings_experiments = Blueprint(
    "settings_experiments", __name__, url_prefix="/settings-experiment/"
)


@settings_experiments.route("/")
def settings_main_page():
    return render_template("settings/main.jinja")


@settings_experiments.route("/pwa")
def settings_pwa():
    return render_template("settings/pwa.jinja")
