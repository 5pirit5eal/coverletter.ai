from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from coverletter.db_models import User
from coverletter import app, db
from coverletter.db_models import User
from flask_login import current_user, login_user, logout_user
from flask import flash, redirect, render_template, url_for, request
import sqlalchemy as sa
from urllib.parse import urlsplit


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    # or use if request.method == "POST" if not using wtf-forms
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        if not login_user(user, remember=form.remember_me.data):
            flash("Login failed.")
            return redirect(url_for("logout"))

        next_page = request.args.get("next")

        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)

    return render_template("auth/login.html", title="Sign In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        if db.session.scalar(sa.select(User).where(User.email == user.email)):
            flash(f"Email {user.email} is already registered.")
            return redirect(url_for("login"))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(f"Hello, {form.name.data}! You are now a registered user.")
        return redirect(url_for("login"))
    return render_template("auth/register.html", title="Register", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


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
#             return redirect(url_for("login"))

#         flash(error)

#     return render_template("auth/register.html")
