"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from app import app
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash
from app.forms import RegistrationForm, LoginForm, NewPostForm
from werkzeug.utils import secure_filename
from . import db
from app.models import Post,Like,Follow,User
import os
from .config import Config


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render Photogram's home page."""
    return render_template('home.html')

@app.route('/explore', methods=['POST', 'GET'])
def explore():
    """Render Photogram's explore page."""
    return render_template('explore.html')

@app.route('/profile')
def profile():
    """Render Photogram's profile page."""
    return render_template('profile.html')

@app.route('/posts/new')
def post():
    """Render Photogram's new post page."""
    form = NewPostForm()
    if form.validate_on_submit():
        photo_file = form.data.photo
        photo_filename = secure_filename(photo_file.filename)
        photo_file.save(os.path.join(Config.UPLOAD_FOLDER, photo_filename))
        caption = form.data.caption
        return redirect(url_for('profile'))
    return render_template('post.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    """Render Photogram's registration page."""
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
        photo_filename = secure_filename(photo_file.filename)
        photo_file.save(os.path.join(Config.UPLOAD_FOLDER, photo_filename))
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Render Photogram's sign in page."""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data.username
        password = form.data.password
        return redirect(url_for('explore'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Logout user."""
    return render_template('logout.html')

@app.route('/users/<userid>')
def display_profile(userid):
    pass
###
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
