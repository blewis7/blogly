from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brockisgood'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.drop_all()
db.create_all()

# Users Route

@app.route('/')
def transfer():
    '''Home page needs to show a list of users'''
    return redirect('/users')


@app.route('/users')
def homepage():
    '''Homepage displays list of users'''
    users = User.query.all()
    return render_template('users/home.html', users=users)


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    '''Show details about a user'''
    user = User.query.get_or_404(user_id)
    return render_template("users/user.html", user=user)


@app.route('/users/new', methods=["GET"])
def new_user_form():
    '''Show the new user form'''
    return render_template('users/new.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    '''Add user to database'''

    new_user = User(
        first_name = request.form["first"],
        last_name = request.form["last"],
        image = request.form["img"] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')
        
@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''Edit user information'''
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    '''Update user to database'''

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    user.image = request.form["img"] or None
    
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    '''Delete User from Database'''

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


# Posts Route


@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    '''Open new post form'''
    user  = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    '''Add post to database'''

    user  = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title = request.form["title"],
        content = request.form["content"],
        user=user,
        tags=tags
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''Show a single post's information'''

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_pst(post_id):
    '''Edit post information'''
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("posts/edit.html", post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    '''Update post to database'''

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    '''Delete Post from Database'''

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


# Tags routes


@app.route('/tags')
def all_tags():
    '''Show a list of all tags'''

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new', methods=["GET"])
def new_tags_form():
    '''Show the new tags form'''
    return render_template('tags/new.html')


@app.route('/tags/new', methods=["POST"])
def create_tags():
    '''Add user to database'''

    new_tag = Tag(
        name = request.form.get("name")
    )

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    '''Show a tag's information and posts with the tag'''

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    '''Edit post information'''
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/edit.html", tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):
    '''Update tag to database'''

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    
    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag.id}')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    '''Delete tag from Database'''

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
