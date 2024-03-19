from collections import OrderedDict
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    DateField,
    IntegerField,
    SelectField,
)
from wtforms.validators import InputRequired, ValidationError, Optional, EqualTo
from coverletter import app, db
from flask_login import login_required, current_user
from coverletter.db_models import User, Resume, ResumeItem
from flask import render_template, redirect, url_for, session
from datetime import datetime, timezone


class ResumeItemForm(FlaskForm):
    title = TextAreaField("Title", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    category = SelectField(
        "Category",
        choices=[
            "-",  # Placeholder
            "education",
            "work",
            "project",
            "skill",
            "language",
            "certification",
            "volunteer",
            "course",
        ],
        validators=[InputRequired()],
    )
    begin_date = DateField("Begin Date", validators=[Optional()])
    end_date = DateField("End Date", validators=[Optional()])
    grade = IntegerField("Grade", validators=[Optional()])
    location = StringField("Location", validators=[Optional()])
    submit = SubmitField("Add Item")

    def validate_category(self, category):
        if category.data == "-":
            raise ValidationError("Please select a category.")
        if category.data == "education" and not self.grade.data:
            raise ValidationError("Grade is required for education items.")
        if category.data in ["work", "project", "volunteer"] and not self.location.data:
            raise ValidationError("Location is required for work, project, and volunteer items.")
        if category.data in ["work", "project", "volunteer"] and not self.begin_date.data:
            raise ValidationError("Begin date is required for work, project, and volunteer items.")
        if category.data in ["work", "project", "volunteer"] and not self.end_date.data:
            raise ValidationError("End date is required for work, project, and volunteer items.")

    def validate_begin_date(self, begin_date):
        if self.end_date.data and begin_date.data > self.end_date.data:
            raise ValidationError("Begin date must be before end date.")

    def validate_end_date(self, end_date):
        if self.begin_date.data and end_date.data < self.begin_date.data:
            raise ValidationError("End date must be after begin date.")


class ResumeForm(FlaskForm):
    language = SelectField(
        "Language",
        choices=["en", "de"],
        validators=[InputRequired()],
    )
    submit = SubmitField("Create Resume")


def get_resume_categories(resume: Resume) -> dict[str, list[ResumeItem]]:
    categories = {item.category for item in resume.resume_items}
    resume_categories = {}

    for category in categories:
        resume_items = sorted(
            [item for item in resume.resume_items if item.category == category],
            key=lambda x: x.begin_date,
            reverse=True,
        )
        resume_items_preview = [
            {
                "title": resume_item.title,
                "description": resume_item.description,
                "begin_date": (
                    resume_item.begin_date.strftime("%m/%y") if resume_item.begin_date else None
                ),
                "end_date": (
                    "- " + resume_item.end_date.strftime("%m/%y") if resume_item.end_date else None
                ),
                "grade": resume_item.grade,
                "location": resume_item.location,
            }
            for resume_item in resume_items
        ]
        resume_categories[category] = resume_items_preview
    return resume_categories


@app.route("/user/<email>")
@login_required
def user(email: str):
    user: User = User.query.filter_by(email=email).first_or_404()
    resume_preview = {}
    for resume in user.resumes:
        resume_categories = get_resume_categories(resume)
        resume_preview[resume] = resume_categories
    return render_template("profile/user.html", user=user, resume_preview=resume_preview)


@app.route("/add_resume/<email>", methods=["GET", "POST"])
@login_required
def add_resume(email: str):
    user = User.query.filter_by(email=email).first_or_404()
    if not user.resumes:
        resume = Resume(language="en", user_id=user.id)
        db.session.add(resume)
        db.session.commit()
    else:
        resume = Resume.query.filter_by(user_id=user.id, language="en").first()
    return redirect(url_for("add_resume_item", resume_id=resume.id))

    form = ResumeForm()
    if form.validate_on_submit():
        resume = Resume(language=form.language.data, user_id=user.id)
        db.session.add(resume)
        db.session.commit()
        return redirect(url_for("user", resume_id=resume.id))

    return render_template("profile/add_resume.html", form=form)


@app.route("/add_resume_item/<resume_id>", methods=["GET", "POST"])
@login_required
def add_resume_item(resume_id: str):
    resume = Resume.query.filter_by(id=resume_id).first_or_404()
    form = ResumeItemForm()
    if form.validate_on_submit():
        resume_item = ResumeItem(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            begin_date=form.begin_date.data,
            end_date=form.end_date.data,
            grade=form.grade.data,
            location=form.location.data,
            resume=resume,
        )
        db.session.add(resume_item)
        db.session.commit()
        session["resume_id"] = resume.id
        return redirect(url_for("user", email=current_user.email))

    return render_template("profile/add_resume_item.html", form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
