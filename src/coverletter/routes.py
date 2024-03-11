from coverletter import app, db
from coverletter.auth import LoginForm, RegisterForm
from coverletter.db_models import User
from flask_login import current_user, login_user, logout_user, login_required
from flask import flash, redirect, render_template, url_for, request
import sqlalchemy as sa
from urllib.parse import urlsplit


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("home/index.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
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
