from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brockisgood'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    '''Home page needs to show a list of users'''
    users = User.query.all()
    return render_template('home.html', users=users)


@app.route('/<int:user_id>')
def show_user_details(user_id):
    '''Show details about a user'''
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


@app.route('/new', methods=["GET"])
def new_user_form():
    '''Show the new user form'''
    return render_template('new.html')


@app.route('/new', methods={"POST"})
def create_user():
    '''Add user to database'''

    new_user = User(
        first_name = request.form["first"],
        last_name = request.form["last"],
        image = request.form["img"] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/')
        
@app.route('/<int:user_id>/edit')
def edit_user(user_id):
    '''Edit user information'''
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route('/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    '''Update user to database'''

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    user.image = request.form["img"] or None
    

    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route('/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    '''Delete User from Database'''

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

    

    

