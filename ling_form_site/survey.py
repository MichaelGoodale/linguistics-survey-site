import os
from flask import Flask, render_template, redirect, url_for, Blueprint, session, request, current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, StringField, PasswordField, validators
from werkzeug.utils import secure_filename
from uuid import uuid1

from .db import db_session
from .models import User, Recording

bp = Blueprint('survey', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'GET' and 'user_id' not in session:
        session['user_id'] = str(uuid1())
        user = User(session['user_id'])
        db_session.add(user)
        db_session.commit()
    return render_template('survey.html')

@bp.route('/upload_audio/<recording>', methods=['POST'])
def upload_audio(recording):
    user = db_session.query(User).filter(User.uuid == session['user_id']).first()
    if user is None:
        return "No user by that id"
    recording_file = request.files["recording"]
    file_path = os.path.join(current_app.instance_path, '{}.wav'.format(uuid1()))
    recording_file.save(file_path)
    user.recordings.append(Recording(recording, file_path))
    db_session.commit()
    return "we did it"
