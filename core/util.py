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
# cython: language_level=3

from services.web.website.models.lesson_models import Lesson


def find_next_lessons(current_lesson_id) -> list:
    """
    When given a lesson id this function can find the next lessons for a user
    """
    the_lesson = Lesson.query.filter_by(lesson_id=current_lesson_id).first()
    next_lessons = the_lesson.goes_to
    next_lessons = next_lessons.split(",")
    return next_lessons


def clean_up(progress):
    """
    Cleans up progress so that progress only displays the users most advanced lessons learned rather that all of them
    """
    cleaned_up = []
    for item in progress:
        in_progress = True
        for thing in find_next_lessons(item):
            if thing in progress:
                in_progress = False
        if in_progress:
            progress.remove(item)
    return cleaned_up


def recommended(progress):
    """
    Finds recommended lessons for a user
    """
    display = []
    for item in progress:
        for lesson in find_next_lessons(item):
            display.append(lesson)
    return display
