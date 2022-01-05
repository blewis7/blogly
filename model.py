from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG = 'https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-4.png'

class User(db.Model):
    '''Creating Users'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMG)


def connect_db(app):
    '''Connect to database.'''

    db.app = app
    db.init_app(app)