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

from services.web.website.bp.experiments.settings_experiment import settings_experiments
from flask import render_template, Blueprint

experiments = Blueprint("experiments", __name__, url_prefix="/experiments/")


@experiments.route("/")
def index():
    return render_template("experiments/experiment_list.html")


@experiments.route("/custom-python-tag")
def custom_python_tag():
    return render_template("experiments/python-code-custom-tag.jinja")


@experiments.route("/right-click")
def right_click():
    return render_template("experiments/right-click-test.jinja")


@experiments.route("/question-creator")
def question_creator():
    return render_template("experiments/question_creator.jinja")


def register_experimental_blueprints(app):
    app.register_blueprint(experiments)
    app.register_blueprint(settings_experiments)
