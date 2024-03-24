from flask_login import current_user, login_required
from flask_wtf import FlaskForm

from coverletter import app, db
from coverletter.db_models import User, Resume, Prompt, CoverLetter, JobPosting, ModelConfig


# @app.route("/coverletters")
# @login_required
# def coverletters():
#     coverletters = current_user.previous_coverletters()
#     return render_template("coverletters.html", coverletters=coverletters)
