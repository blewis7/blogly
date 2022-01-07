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


class PostTag(db.Model):
    '''Class creates a many-to-many relationship between Post and Tag'''
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    '''Creating Tags'''

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', cascade='all, delete', backref='tags')


def connect_db(app):
    '''Connect to database.'''

    db.app = app
    db.init_app(app)