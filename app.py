"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'key34'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

with app.app_context():
    connect_db(app)
    db.create_all()


@app.route('/')
def home_page():
    '''Redirect to list of users'''
    return redirect('/users')


@app.route('/users')
def users_index():
    '''Show all users'''

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('/users/users.html', users=users)


@app.route('/users/new', methods=['GET'])
def create_user():
    '''Show an add form for users'''

    return render_template('/users/create_user.html')


@app.route('/users/new', methods=['POST'])
def created_user():
    '''Process the add form, adding a new user and going back to /users'''

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''Show information about the given user.'''

    user = User.query.get_or_404(user_id)
    return render_template('/users/show_user.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''Show the edit page for a user.'''

    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    '''Process the edit form, returning the user to the /users page.'''

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Delete the user.'''

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# part two - posts route


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    '''Show form to add a post for that user.'''

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def posts_new(user_id):
    '''Creating a new post from a specific user'''

    user = User.query.get_or_404(user_id)

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''Show a post'''

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    '''Show form to edit a post, and to cancel (back to user page).'''

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    '''Handle editing of a post. Redirect back to the post view'''

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Delete the post'''

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')
