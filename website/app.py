import os
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, StringField, PasswordField, validators
from werkzeug.utils import secure_filename

app = Flask(__name__, instance_path="/home/michael/Documents/Schoolwork/U3/Winter/ling-521/instance_path")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class LinguisticForm(FlaskForm):
    name = StringField('name', [validators.Length(min=3, max=100)])
    audio = FileField(validators=[FileRequired()])


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/survey', methods=["GET", "POST"])
def survey():
    form = LinguisticForm()
    if form.validate_on_submit():
        f = form.audio.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'audio_files', filename
        ))
        return redirect(url_for('index'))
    return render_template('survey.html', form=form)
