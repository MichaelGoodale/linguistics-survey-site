import os
import json
from wtforms import Form, RadioField, SelectMultipleField, SelectField, TextAreaField, HiddenField, StringField
from wtforms.widgets import CheckboxInput, ListWidget

def generate_survey_form(survey_path):
    with open(survey_path, "r") as f:
        survey = json.load(f)

    form_pages = []
    for page_number, page in enumerate(survey["pages"]):
        class F(Form):
            pass
        for question in page:
            q_type = question["type"]
            q_name = question["name"]
            q_text = question["question"]

            if q_type == "multiple_choice":
                q_answers = question["answers"]
                field = SelectMultipleField(q_text, choices=[(i, x) for i, x in enumerate(q_answers)], \
                        option_widget=CheckboxInput(),
                        widget=ListWidget(prefix_label=False))
            elif q_type == "single_choice":
                q_answers = question["answers"]
                field = RadioField(q_text, choices=[(i, x) for i, x in enumerate(q_answers)])
            elif q_type == "string":
                field = StringField(q_text)
            elif q_type == "textbox":
                field = TextAreaField(q_text)
            elif q_type == "dropdown":
                q_answers = question["answers"]
                field = SelectField(q_text, choices=[(i, x) for i, x in enumerate(q_answers)])
            elif q_type == "recording":
                field = HiddenField(q_text)
            else:
                raise KeyError(f"Question type {q_type} for {q_name} is not yet implemented")
            setattr(F, q_name, field)
        form_pages.append(F)
    return form_pages
