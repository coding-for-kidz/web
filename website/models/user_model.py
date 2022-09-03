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

from datetime import datetime

from flask_login import UserMixin

from services.web.website.models.db import database


class User(database.Model, UserMixin):
    """The User db table"""

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String, unique=True)
    password = database.Column(database.String)
    email = database.Column(database.String)
    # wants = db.Column(db.String, default="")
    top_progress = database.Column(database.String, default="")
    full_progress = database.Column(database.String, default="")
    date_joined = database.Column(database.DateTime, default=datetime.now)
    about = database.Column(database.Text, default="")
    grade = database.Column(database.String, default="")
    image = database.Column(
        database.String,
        default="https://lh6.googleusercontent.com/-9-T7Yc3MUlU/AAAAAAAAAAI/AAAAAAAAAAA/CJDv3ZmEmkI/s64c",
    )
    admin = database.Column(database.Integer, default=0)
    tags = database.Column(database.String, default="")
    # notifications = database.Column(database.String, default="")
