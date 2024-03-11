from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from coverletter.db_models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")

    def validate_email(self, email):
        """Automatically validate if email address is not already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


# import functools

# from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
# from werkzeug.security import check_password_hash, generate_password_hash

# from coverletter import db
# import coverletter.db_models as models
# from sqlalchemy import select

# bp = Blueprint("auth", __name__, url_prefix="/auth")


# @bp.route("/register", methods=("GET", "POST"))
# def register():
#     if request.method == "POST":
#         user = models.User(
#             name=request.form["name"],
#             email=request.form["email"],
#             password=request.form["password"],
#         )
#         error = None

#         if not user.name:
#             error = "Username is required."
#         elif not user.password:
#             error = "Password is required."
#         elif not user.email:
#             error = "Email is required."
#         elif (
#             db.session.execute(
#                 select(models.User).where(models.User.email == user.email)
#             ).fetchone()
#             is not None
#         ):
#             error = f"Email {user.email} is already registered."

#         if error is None:
#             user.password = generate_password_hash(user.password)
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for("auth.login"))

#         flash(error)

#     return render_template("auth/register.html")
