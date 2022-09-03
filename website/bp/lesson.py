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

from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.exceptions import abort

from services.web.core import interpretlesson
from services.web.website import cache
from services.web.website.models import database
from services.web.website.models.lesson_models import Lesson, Folder

lesson = Blueprint("lesson", __name__)


class LessonCardInfo:
    """
    Card info for a lesson
    """

    def __init__(self, title, subtitle, link, image, lesson_id):
        self.title = title
        self.subtitle = subtitle
        self.image = image
        self.link = link
        self.lesson_id = lesson_id

    def __eq__(self, other):
        if (
            (self.title != other.title)
            or (self.subtitle != other.subtitle)
            or (self.image != other.image)
            or (self.link != other.link)
            or (self.lesson_id != other.lesson_id)
        ):
            return False
        return True


@lesson.route("/learn", endpoint="learn")
@cache.cached(timeout=1)
def learn():
    lessons_for_you = []
    all_lessons_temp = Lesson.query.all()
    all_lessons = []
    for item in all_lessons_temp:
        all_lessons.append(
            LessonCardInfo(
                item.title,
                item.subtitle,
                "/lesson/" + str(item.lesson_id),
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
                "/folder/" + str(item.folder_id),
                item.image,
                item.folder_id,
            )
        )
    return render_template(
        "learn/learn.jinja",
        lessons_for_you=lessons_for_you,
        all_lessons=all_lessons,
        all_folders=all_folders,
    )


# lessons
@lesson.route("/lesson/<lesson_id>/")
@cache.cached(timeout=3600)
def access_lesson(lesson_id: str):
    """
    :type lesson_id: int
    """
    lesson_id = str(lesson_id)
    while len(lesson_id) < 5:
        lesson_id = "0" + lesson_id
    lesson_to_render = Lesson.query.filter_by(lesson_id=lesson_id).first()
    if lesson_to_render is None:
        return abort(404)
    if current_user.is_authenticated:
        current_user.top_progress += "," + str(lesson_to_render.id)
        current_user.full_progress += "," + str(lesson_to_render.id)
        database.session.commit()
    lesson_to_render = interpretlesson.Lesson(
        lesson_to_render.lesson_id,
        lesson_to_render.title,
        lesson_to_render.subtitle,
        lesson_to_render.image,
        lesson_to_render.body,
        lesson_to_render.goes_to,
        lesson_to_render.questions,
    )
    return render_template("learn/card_temp.jinja", l=lesson_to_render)


@lesson.route("/folder/<int:folder_id>/")
def view_folder(folder_id: int):
    folder_to_render = Folder.query.filter_by(folder_id=folder_id).first()
    lessons_in_folder = Lesson.query.filter_by(folder_id=folder_id).all()
    folders_in_folder = Folder.query.filter_by(parent_folder_id=folder_id).all()
    if folder_to_render is None:
        abort(404)
    else:
        return render_template(
            "learn/folder_temp.jinja",
            f=folder_to_render,
            lif=lessons_in_folder,
            fif=folders_in_folder,
        )
