from datetime import datetime, timezone

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

from coverletter import app, db
from coverletter.db_models import User


class EditProfileForm(FlaskForm):
    name = TextAreaField("Name", validators=[InputRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.about_me.data = current_user.about_me
    return render_template("profile/edit_profile.html", title="Edit Profile", form=form)


@app.route("/user/<email>")
@login_required
def user(email: str):
    user: User = User.query.filter_by(email=email).first_or_404()
    resume_preview = {}
    for resume in user.resumes:
        resume_categories = resume.get_items_per_category()
        resume_preview[resume] = resume_categories
    return render_template("profile/user.html", user=user, resume_preview=resume_preview)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
