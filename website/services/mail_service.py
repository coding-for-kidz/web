from flask_mail import Mail


class MailService:
    """Cache manager"""

    def __init__(self):
        self._mail = Mail()

    def init_mail(self, app):
        self._mail.init_app(app)

    def get_mail(self):
        return self._mail
