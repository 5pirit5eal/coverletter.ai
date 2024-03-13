from coverletter import app, db
from flask_login import login_required, current_user
from coverletter.db_models import User, Resume, ResumeItem
from flask import render_template, redirect, url_for


@app.route("/quiz/<email>")
@login_required
def quiz(email: str):
    user = User.query.filter_by(email=email).first_or_404()
    # get resume items for newest resume
    if user.resumes:
        resume_items = ResumeItem.query.filter_by(resume_id=user.resumes[-1].id).all()
    else:
        resume_items = []

    return render_template("profile/user.html", user=user, resume_items=resume_items)
