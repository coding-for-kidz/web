from flask import Blueprint, redirect, render_template, request

from services.web.website.bp.lesson import LessonCardInfo
from services.web.website.models import database
from services.web.website.models.lesson_models import Lesson, Folder
from services.web.core.wrappers import admin_only

admin_learn = Blueprint("admin_learn", __name__, url_prefix="/admin-site/lesson/")


@admin_learn.route("/")
@admin_only
def manage_lessons():
    """Admin Learn Page"""
    all_lessons_temp = Lesson.query.all()
    all_lessons = []
    for item in all_lessons_temp:
        all_lessons.append(
            LessonCardInfo(
                item.title,
                item.subtitle,
                "/admin-site/lesson/" + str(item.lesson_id),
                item.image,
                item.lesson_id,
            )
        )
    all_folders_temp = Folder.query.filter_by(parent_folder_id=0).all()
    all_folders = []
    for item in all_folders_temp:
        all_folders.append(
            LessonCardInfo(
                item.title,
                item.subtitle,
                "/admin-site/folder/" + str(item.folder_id),
                item.image,
                item.folder_id,
            )
        )
    return render_template(
        "learn/learn.jinja", all_lessons=all_lessons, all_folders=all_folders
    )


@admin_learn.route("/create/", methods=["GET", "POST"])
@admin_only
def create_lesson():
    error = ""
    lesson = Lesson()
    if request.method == "POST":
        lesson.lesson_id = request.form["lesson_id"]
        lesson.folder_id = request.form["folder_id"]
        lesson.title = request.form["title"]
        lesson.subtitle = request.form["subtitle"]
        lesson.image = request.form["image"]
        lesson.body = request.form["body"]
        lesson.goes_to = request.form["goes_to"]
        database.session.add(lesson)
        database.session.commit()
        return redirect("/admin-site/learn/")
    else:
        return render_template(
            "admin/admin_lesson_temp.jinja", lesson=lesson, create=True, error=error
        )


@admin_learn.route("/edit/<int:lesson_id>/", methods=["GET", "POST"])
@admin_only
def edit_lesson(lesson_id: int):
    """Admin interface for editing a lesson"""
    error = ""
    lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()
    if lesson is None:
        return redirect("/admin-site/create-lesson/")
    if request.method == "POST":
        lesson.lesson_id = request.form["lesson_id"]
        lesson.folder_id = request.form["folder_id"]
        lesson.title = request.form["title"]
        lesson.subtitle = request.form["subtitle"]
        lesson.image = request.form["image"]
        lesson.body = request.form["body"]
        lesson.goes_to = request.form["goes_to"]
        database.session.commit()
        return redirect("/admin-site/learn")
    else:
        return render_template(
            "admin/admin_lesson_temp.jinja",
            lesson=lesson,
            create=False,
            error=error,
        )


@admin_learn.route("/delete/<int:lesson_id>/")
@admin_only
def delete_lesson(lesson_id: int):
    """Deletes Lesson"""
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    database.session.delete(lesson)
    database.session.commit()
    return redirect("/admin-site/learn/")
