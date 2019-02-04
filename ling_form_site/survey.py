import os
from flask import Flask, render_template, redirect, url_for, Blueprint, session, request, current_app, abort
from wtforms import BooleanField, StringField, PasswordField, validators
from werkzeug.utils import secure_filename
from uuid import uuid1

from .db import db_session
from .models import User, Recording
from .utils import generate_survey_form

bp = Blueprint('survey', __name__)
surveys = {}

def get_survey(survey_name):
    if survey_name in surveys:
        return surveys[survey_name]

    survey_path = os.path.join(current_app.instance_path, "surveys", survey_name)
    if not os.path.isfile(survey_path):
        return None

    surveys[survey_name] = generate_survey_form(os.path.join(survey_path))
    return surveys[survey_name]

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/survey/<survey_name>/<int:page>', methods=['GET', 'POST'])
def survey(survey_name, page):
    form = get_survey(survey_name)
    if form is None or page < 0 or page >= len(form):
        abort(404)
    if request.method == 'GET' and 'user_id' not in session:
        session['user_id'] = str(uuid1())
        user = User(session['user_id'])
        db_session.add(user)
        db_session.commit()
    return render_template('survey.html', form=form[page]())

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
