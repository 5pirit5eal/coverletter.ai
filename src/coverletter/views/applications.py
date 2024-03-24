from flask import redirect, render_template, session
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, Optional, ValidationError
import os

from coverletter import app, db
from coverletter.db_models import (
    User,
    Resume,
    Prompt,
    CoverLetter,
    JobPosting,
    ModelConfig,
    ResumeItem,
)


# @app.route("/coverletters")
# @login_required
# def coverletters():
#     """Function that creates an log of previously created coverletters."""
#     coverletters = current_user.previous_coverletters()
#     return render_template("coverletters.html", coverletters=coverletters)


class CreateCoverLetterForm(FlaskForm):
    company = TextAreaField("Company Name")
    posting_url = TextAreaField("Job Posting URL", validators=[Optional()])
    posting_text = TextAreaField("Job Posting Text", validators=[InputRequired()])
    posting_date = DateField("Job Posting Date", validators=[Optional()])
    language = SelectField("Language", choices=["EN", "DE", "Other"], validators=[InputRequired()])
    location = location = StringField("Location", validators=[Optional()])
    submit = SubmitField("Create Coverletter")

    def validate_language(self, language):
        if not Resume.query.filter_by(
            user=current_user, language=language.data.lower()
        ).one_or_none():
            raise ValidationError(
                "No resume was added for this language! "
                "Please select another or create a resume for this language."
            )


@app.route("create")
@login_required
def create():
    form = CreateCoverLetterForm()

    if form.validate_on_submit():
        posting = JobPosting()
        pass

    return render_template("applications/create_letter.html", form=form)


def compose_prompt(job_posting: JobPosting, resume: Resume, user: User) -> str:
    prompt = (
        "Your task is to generate a cover letter for applicant "
        + user.name
        + " and company "
        + (job_posting.company if job_posting.company else "")
    )

    prompt += "\n for the following application: \n" + job_posting.text

    prompt += "\n Based on the following CV: \n" + create_resume_table(resume)
    prompt += "\n It is crucial to not hallucinate skills or experiences that are not present in the CV! Try to make the cover letter as relevant as possible. \n"
    return prompt


def create_resume_table(resume: Resume):
    resume_items: list[ResumeItem] = resume.resume_items

    resume_items.sort(key=lambda item: item.begin_date)
    resume_items.sort(key=lambda item: item.category)

    # Group resume items by category
    grouped_resume_items = {}
    for item in resume_items:
        category = item.category
        if category not in grouped_resume_items:
            grouped_resume_items[category] = []
        grouped_resume_items[category].append(item)

    # Create a markdown table from the grouped and sorted resume items
    table = "| Category | Title | Description | Begin Date | End Date | Grade | Location |\n"
    table += "|----------|-------|-------------|------------|----------|-------|----------|\n"

    for category, items in grouped_resume_items.items():
        for item in items:
            title = item.title
            description = item.description
            begin_date = item.begin_date if item.begin_date else ""
            end_date = item.end_date if item.end_date else ""
            grade = item.grade if item.grade else ""
            location = item.location if item.location else ""

            table += f"| {category} | {title} | {description} | {begin_date} | {end_date} | {grade} | {location} |\n"

    return table


def request_coverletter(prompt) -> str:
    # TODO: Change to requests and REST, not SDK
    from vertexai.language_models import TextGenerationModel

    model = TextGenerationModel.from_pretrained("text-bison@002")

    translate_client = translate.Client()
    prompt = translate_client.translate(prompt, target_language="de")

    response = model.predict(prompt, max_output_tokens=1024)
    for candidate in response.candidates:
        print(candidate)
