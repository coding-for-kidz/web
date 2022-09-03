from datetime import datetime

from services.web.website.models.db import database


class Folder(database.Model):
    id = database.Column(
        database.Integer, primary_key=True, autoincrement=True, unique=True
    )
    folder_id = database.Column(database.Integer, primary_key=True, unique=True)
    parent_folder_id = database.Column(database.Integer, default=0)
    title = database.Column(database.String, unique=True)
    subtitle = database.Column(database.String)
    image = database.Column(database.String)
    content = database.Column(database.String)


class LearningPath(database.Model):
    id = database.Column(
        database.Integer, primary_key=True, autoincrement=True, unique=True
    )
    title = database.Column(database.String)
    description = database.Column(database.String)


class Lesson(database.Model):
    id = database.Column(
        database.Integer, primary_key=True, autoincrement=True, unique=True
    )
    lesson_id = database.Column(database.Integer, primary_key=True, unique=True)
    # goes_to = database.relationship("GoesToLesson", backref="Lesson", lazy=True)
    goes_to = database.Column(database.String)
    title = database.Column(database.String, unique=True)
    subtitle = database.Column(database.String)
    image = database.Column(database.String)
    body = database.Column(database.Text)
    folder_id = database.Column(
        database.Integer, database.ForeignKey("folder.folder_id"), default=0
    )
    questions = database.relationship("Question", backref="Lesson", lazy=True)
    comments = database.relationship("Comment", backref="Lesson", lazy=True)


class GoesToLesson(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    lesson_id = database.Column(
        database.Integer, database.ForeignKey("lesson.lesson_id")
    )
    lesson = database.Column(database.Integer, database.ForeignKey("lesson.lesson_id"))


class Question(database.Model):
    """Question Model"""

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    for_lesson_id = database.Column(
        database.Integer, database.ForeignKey("lesson.lesson_id"), nullable=False
    )
    answers = database.relationship("Answer", backref="Question", lazy=True)
    content = database.Column(database.String)


class Answer(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    question_id = database.Column(database.Integer, database.ForeignKey("question.id"))
    correct = database.Column(database.Boolean, primary_key=True, default=False)
    content = database.Column(database.String)


class Comment(database.Model):
    """Comment on a lesson"""

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    created_by_user_id = database.Column(
        database.Integer, database.ForeignKey("user.id")
    )
    date_created = database.Column(database.DateTime, default=datetime.now)
    lesson_id = database.Column(
        database.Integer, database.ForeignKey("lesson.lesson_id")
    )
    content = database.Column(database.String)
