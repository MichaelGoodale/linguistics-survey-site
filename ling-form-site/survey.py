import os
from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, StringField, PasswordField, validators
from werkzeug.utils import secure_filename

bp = Blueprint('survey', __name__, url_prefix='/survey')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/survey', methods=['GET', 'POST'])
def survey():
    return render_template('survey.html')

@bp.route('/upload_audio/<uuid:user>/<recording>', methods=['POST'])
def upload_audio(user, recording):
    return user
