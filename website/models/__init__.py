"""db models"""
from services.web.website.models.db import database
from datetime import datetime

# image_data = file
# >>> encoded = base64.b64encode(image_data) # Creates a bytes object
# >>> 'data:image/png;base64,{}'.format(encoded)
# "data:image/png;base64,b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='"
#
#
# # Calling .decode() gets us the right representation
# >>> encoded = base64.b64encode(image_data).decode('ascii')
# >>> 'data:image/png;base64,{}'.format(encoded)


class Image(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    content = database.Column(database.String)


class Error(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    url = database.Column(database.String)
    error = database.Column(database.Text)
    user_id = database.Column(
        database.Integer, database.ForeignKey("user.id"), primary_key=True
    )


class NotFoundError(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    url = database.Column(database.String, primary_key=True)
    reporter = database.Column(
        database.Integer, database.ForeignKey("user.id"), primary_key=True
    )
    date_created = database.Column(database.DateTime, default=datetime.now)


class Article(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    created_by_admin_id = database.Column(
        database.Integer, database.ForeignKey("user.id")
    )
    date_created = database.Column(database.DateTime, default=datetime.now)
    title = database.Column(database.Text)
    subtitle = database.Column(database.Text)
    content = database.Column(database.Text)
    comments = database.relationship("ArticleComment", backref="Article", lazy=True)


class ArticleComment(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    date_created = database.Column(database.DateTime, default=datetime.now)
    created_by_user_id = database.Column(
        database.Integer, database.ForeignKey("user.id")
    )
    lesson_id = database.Column(database.Integer, database.ForeignKey("article.id"))
    content = database.Column(database.Text)


class Project(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    date_created = database.Column(database.DateTime, default=datetime.now)
    created_by_user_id = database.Column(
        database.Integer, database.ForeignKey("user.id")
    )
    name = database.Column(database.String)
    private = database.Column(database.Boolean, default=True)
    remix = database.Column(database.String, default="None")
    files = database.relationship("File", backref="Project", lazy=True)
    likes = database.Column(database.Integer, primary_key=True, default=0)
    stars = database.Column(database.Integer, primary_key=True, default=0)


class File(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    project_id = database.Column(database.Integer, database.ForeignKey("project.id"))
    name = database.Column(database.Text)
    contents = database.Column(database.Text)
