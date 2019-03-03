import os
import json
from wtforms import Form, RadioField, SelectMultipleField, SelectField, TextAreaField, HiddenField, StringField, IntegerField, validators
from wtforms.widgets import CheckboxInput, ListWidget

def get_survey_name(survey_path):
    with open(survey_path, "r") as f:
        survey = json.load(f)
    return survey["name"]

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

            if "required" in question and question["required"] == "false":
                validators_to_use = []
            else:
                validators_to_use = [validators.InputRequired(message="This question is required")]

            if "validators" in question:
                #This hellish comprehension makes a list of validator objects
                #with a given name, and their associated parameters
                validators_to_use += [getattr(validators, validator)(**params) for validator, params in question["validators"].items()]

            if q_type == "multiple_choice":
                q_answers = question["answers"]
                field = SelectMultipleField(q_text, validators_to_use, choices=[(str(x), str(x)) for i, x in enumerate(q_answers)], \
                        option_widget=CheckboxInput(),
                        widget=ListWidget(prefix_label=False),
                        render_kw={"data-type": "multiple_choice"})
            elif q_type == "single_choice":
                q_answers = question["answers"]
                field = RadioField(q_text, validators_to_use, choices=[(str(x), str(x)) for i, x in enumerate(q_answers)], \
                       render_kw={"data-type": "single_choice"})
            elif q_type == "likert":
                q_answers = question["answers"]
                min_label = question["minmax"][0]
                max_label = question["minmax"][1]
                field = RadioField(q_text, validators_to_use, choices=[(str(x), str(x)) for i, x in enumerate(q_answers)], \
                       render_kw={"data-type": "likert", "data-min": min_label, "data-max":max_label})
            elif q_type == "string":
                field = StringField(q_text, validators_to_use, render_kw={"data-type": "string"})
            elif q_type == "integer":
                field = IntegerField(q_text, validators_to_use, render_kw={"data-type": "integer"})
            elif q_type == "textbox":
                field = TextAreaField(q_text, validators_to_use, render_kw={"data-type": "textbox"})
            elif q_type == "dropdown":
                q_answers = question["answers"]
                field = SelectField(q_text, validators_to_use, choices=[(None, '')]+[(str(x), str(x)) for i, x in enumerate(q_answers)], \
                        render_kw={"data-type": "dropdown"})
            elif q_type == "reading":
                field = HiddenField(q_text, validators_to_use, render_kw={"data-type": "reading", "data-prompt": question["prompt"]})
            elif q_type == "wordlist":
                field = HiddenField(q_text, validators_to_use, render_kw={"data-type": "wordlist", "data-word_list": question["words"]})
            else:
                raise KeyError(f"Question type {q_type} for {q_name} is not yet implemented")
            setattr(F, q_name, field)
        form_pages.append(F)
    return form_pages
