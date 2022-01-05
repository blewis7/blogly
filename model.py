import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey

db = SQLAlchemy()

DEFAULT_IMG = 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-4.png'

class User(db.Model):
    '''Creating Users'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, default=DEFAULT_IMG)

    posts = db.relationship("Post", backref='user', cascade='all, delete-orphan')

class Post(db.Model):
    '''Creating posts'''

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def connect_db(app):
    '''Connect to database.'''

    db.app = app
    db.init_app(app)