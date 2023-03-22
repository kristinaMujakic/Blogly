"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)


DEFAULT_IMAGE_URL = 'https://cdn-icons-png.flaticon.com/512/149/149071.png'


class User(db.Model):
    '''Blog"s user'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):

        return f"{self.first_name} {self.last_name}"
