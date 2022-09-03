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

from flask import Blueprint, request, redirect, render_template
from services.web.website.models import database

from services.web.website.bp.admin.user import admin_user
from services.web.website.bp.admin.learn import admin_learn
from services.web.website.models.lesson_models import Lesson, Folder
from services.web.core.wrappers import admin_only

admin = Blueprint("admin", __name__, url_prefix="/admin-site/")


@admin.route("/")
@admin_only
def admin_home():
    """Admin Home"""
    return render_template("admin/admin_home.jinja")


@admin.route("/create-folder/", methods=["GET", "POST"])
@admin_only
def create_folder():
    error = ""
    folder = Folder()
    folder.parent_folder_id = 0
    if request.method == "POST":
        folder.folder_id = request.form["folder_id"]
        folder.parent_folder_id = request.form["parent_folder_id"]
        folder.title = request.form["title"]
        folder.subtitle = request.form["subtitle"]
        folder.image = request.form["image"]
        folder.content = request.form["body"]
        database.session.add(folder)
        database.session.commit()
        return redirect("/admin-site/learn/")
    else:
        return render_template(
            "admin/admin_folder_temp.jinja",
            error=error,
            create=True,
            folder=folder,
            lif=[],
        )


@admin.route("/folder/<int:folder_id>/", methods=["GET", "POST"])
@admin_only
def edit_folder(folder_id: int):
    error = ""
    folder = Folder.query.filter_by(folder_id=folder_id).first()
    lessons_in_folder = Lesson.query.filter_by(folder_id=0).all()
    folders_in_folder = Folder.query.filter_by(parent_folder_id=folder_id).all()
    if folder is None:
        return redirect("/admin-site/create-folder/")
    if request.method == "POST":
        folder.folder_id = request.form["folder_id"]
        folder.parent_folder_id = request.form["parent_folder_id"]
        folder.title = request.form["title"]
        folder.subtitle = request.form["subtitle"]
        folder.image = request.form["image"]
        folder.content = request.form["body"]
        database.session.commit()
        return redirect("/admin-site/learn/")
    else:
        return render_template(
            "admin/admin_folder_temp.jinja",
            error=error,
            create=False,
            folder=folder,
            lif=lessons_in_folder,
            fif=folders_in_folder,
        )


@admin.route("/delete-folder/<int:lesson_id>/")
@admin_only
def delete_folder(lesson_id: int):
    """Deletes Folder"""
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    database.session.delete(lesson)
    database.session.commit()
    return redirect("/admin-site/learn/")


@admin.route("/articles/")
@admin_only
def manage_articles():
    return render_template("admin/admin_articles.jinja")


@admin.route("/projects/")
@admin_only
def manage_projects():
    return render_template("admin/admin_projects.jinja")


@admin.route("/execute/")
@admin_only
def execute_code():
    # put code here
    return "nothing here"


def register_admin_blueprints(app):
    app.register_blueprint(admin)
    app.register_blueprint(admin_learn)
    app.register_blueprint(admin_user)
