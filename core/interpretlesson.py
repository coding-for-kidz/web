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
"""Interprets a lesson string"""

import random


class Question:
    """Question class"""

    def __init__(self, content, answer_list, correct_answer):
        self.content = content
        self.correct_answer = correct_answer
        random.shuffle(answer_list)
        self.answer_list = answer_list


class Lesson:
    """Lesson class"""

    def __init__(self, lesson_id, title, subtitle, image, content, goes_to, questions):
        self.lesson_id = lesson_id
        self.title = title
        self.subtitle = subtitle
        self.image = image
        self.content = content
        self.goes_to = goes_to.split(",")  # example: 00004,00010,00020
        self.questions = []
        for item in questions:
            self.questions.append(
                Question(
                    item.content,
                    item.answers.filter_by(question_id=True).first(),
                    item.answers.all(),
                )
            )
