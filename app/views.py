"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
import jwt
from functools import wraps
from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash,g,send_from_directory
from app.forms import RegistrationForm, LoginForm, NewPostForm
from werkzeug.utils import secure_filename
from . import db
from app.models import Post,Like,Follow,User
import os
from .config import Config
from datetime import datetime, timedelta
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf.csrf import generate_csrf
from werkzeug.security import check_password_hash

# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated

###
# Routing for your application.
###
@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

# USER REGISTRATION 
@app.route('/api/v1/register', methods=['POST'])
def register():
    """Register a user"""
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.data.username
        password = form.data.password
        first_name = form.data.first_name
        last_name = form.data.last_name
        email = form.data.email
        location = form.data.location
        bio = form.data.bio
        photo_file = form.data.photo
        joined_on = datetime.utcnow()
        photo_filename = secure_filename(photo_file.filename)
        photo_file.save(os.path.join(app.config.UPLOAD_FOLDER, photo_filename))

        user = User(username,password,first_name,last_name,email,location,bio,photo_file,joined_on)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "User successfully registered.",
            "username": username,
            "password": password,
            "firstname": first_name,
            "lastname": last_name,
            "email": email,
            "location": location,
            "biography": bio,
            "profile_photo":  photo_filename,
            "joined_on": joined_on
        }), 201
    errors = form_errors(form)
    return jsonify(errors=errors), 400

# USER LOGIN 
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Login an existing User"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data.username
        password = form.data.password
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            jwt_token = generate_token(user.id)
            return jsonify({
                "message": "User successfully logged in.",
                "token": jwt_token
            }), 200
        return jsonify(errors=["Invalid username or password"])
    errors = form_errors(form)
    return jsonify(errors=errors), 400
    
# User Logout
@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout an existing user"""
    logout_user()
    return jsonify({
        "message": "User successfully logged out."
    }), 200

# User Details
@app.route('/api/v1/users/<user_id>', methods=['GET'])
@login_required
@requires_auth
def get_user_details(user_id):
    """Returns details of the user"""
    user_details = db.session.execute(db.select(User).filter_by(id=int(user_id))).scalar()
    user_posts = db.session.execute(db.select(Post).filter_by(user_id=int(user_id))).scalars()
    posts = []
    for post in user_posts:
        posts.append({
            "id": post.id,
            "user_id": post.user_id,
            "photo": post.photo,
            "description": post.caption,
            "created_on": post.created_on,
        })
    return jsonify({
        "id": user_details.id,
        "username": user_details.username,
        "firstname": user_details.firstname,
        "lastname": user_details.lastname,
        "email": user_details.email,
        "location": user_details.location,
        "biography": user_details.biography,
        "profile_photo": user_details.profile_photo,
        "joined_on": user_details.joined_on,
        "posts": posts
    }), 200
#------------------------------ POSTS ----------------------------------------------#
#View User Posts
@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
@login_required
@requires_auth
def get_posts(user_id):
    """Get a list of all posts by a specific user."""
    user_posts = db.session.execute(db.select(Post).filter_by(user_id=user_id)).scalars()
    posts = []
    for post in user_posts:
        posts.append({
            "id": post.id,
            "user_id": post.user_id,
            "photo": post.photo,
            "description": post.caption,
            "created_on": post.created_on,
        })
    return jsonify(posts=posts), 200

#Create User Posts  
@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@login_required
@requires_auth
def add_post(user_id):
    """Create a new post for the current logged in user."""
    postForm = NewPostForm()
    if postForm.validate_on_submit():
        photo = postForm.photo.data
        caption = postForm.caption.data
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        created_on = datetime.utcnow()
        post = Post(caption,photo_filename,user_id,created_on)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            "message": "Successfully created a new post"
        }), 201
    errors = form_errors(postForm)
    return jsonify(errors=errors), 400


#---------------------------------------Follow Users-------------------------------------

#Follow a user 
@app.route('/api/v1/users/<user_id>/follow', methods=['POST'])
@login_required
@requires_auth
def follow(user_id):
    """Follow the user whos profile you are viewing."""
    #NOTE User ID is the person being followed 
    follow = Follow(user_id=user_id, follower_id=int(current_user.get_id()))
    db.session.add(follow)
    db.session.commit()
    return jsonify({
        "message": "You are now following that user."
    }), 201

#TODO Get number of followers
@app.route('/api/v1/users/<user_id>/follow', methods=['GET'])
@login_required
@requires_auth
def get_num_followers(user_id):
    followers_count = db.session.execute(db.select(Follow).filter_by(user_id=user_id)).count()

    # Return the result as a JSON object
    return jsonify({"followers": followers_count})

#----------------------------View Posts------------------------------------# 

#View all Posts by all Users 
@app.route('/api/v1/posts', methods=['GET'])
@login_required
@requires_auth
def get_all_posts():
    """View all posts by all registered users in the system."""
    posts = db.session.execute(db.select(Post)).scalars()
    all_posts = []
    for post in posts:
        likes = db.session.execute(db.select(Like).filter_by(id=post.id)).scalars()
        all_posts.append({
            "id": post.id,
            "user_id": post.user_id,
            "photo": post.photo,
            "caption": post.caption,
            "created_on": post.created_on,
            "likes": len([like for like in likes])
        })
    return jsonify(all_posts), 200
#---------------------------------------Like Posts----------------------------------#

#Like a Specific Post
@app.route('/api/v1/posts/<post_id>/like', methods=['POST'])
@login_required
@requires_auth
def like(post_id):
    """Like a specific Post by the logged in User"""
    post = db.session.execute(db.select(Post).filter_by(id=post_id)).scalar()
    if post is not None:
        likes = db.session.execute(db.select(Like).filter_by(post_id=post.id)).scalars()
        if post is not None:
            uid = int(current_user.get_id())
            like = Like(post_id, uid)
            db.session.add(like)
            db.session.commit()
            return jsonify({
                "message": "Post liked!",
                "likes": len([like for like in likes]) + 1
            }), 201

###---------------------------------------------------------------------------------------------------
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

def generate_token(uid):
    timestamp = datetime.utcnow()
    payload = {
        "subject": uid,
        "iat": timestamp,
        "exp": timestamp + timedelta(minutes=60)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

@app.route("/api/v1/images/<path:filename>")
def getImage(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).filter_by(id=user_id)).scalar()


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})