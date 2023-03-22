"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'key34'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()


@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def users_index():

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', users=users)


@app.route('create_user', methods=['GET'])
def create_user():
    '''Renders a form to create a new user'''

    return render_template('create_user.html')


@app.route('/create_user', methods=['POST'])
def created_user():
    '''Handles form subbmission'''

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/<int:user_id>')
def show_user(user_id):
    '''Render a page with info for a specific user'''

    user = User.query.get_or_404(user_id)
    return render_template('show_user.html', user=user)


@app.route('/<int:user_id>/edit')
def edit_user(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('/edit.html', user=user)


@app.route('/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
