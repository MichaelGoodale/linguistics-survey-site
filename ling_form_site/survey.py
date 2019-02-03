import os
from flask import Flask, render_template, redirect, url_for, Blueprint, session, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, StringField, PasswordField, validators
from werkzeug.utils import secure_filename
from uuid import uuid1

from .db import db_session
from .models import User
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
    print(session)
    return render_template('survey.html')

@bp.route('/upload_audio/<uuid:user>/<recording>', methods=['POST'])
def upload_audio(user, recording):
    return user
