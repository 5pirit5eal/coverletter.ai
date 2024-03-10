from coverletter import app
from coverletter.auth import LoginForm, RegisterForm
from flask import flash, redirect, render_template, url_for


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Miguel"}
    return render_template("tutorial/index.html", title="Home", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            (
                f"Login requested from user {form.email.data}, "
                f"remember me {form.remember_me.data}"
            ),
        )
        return redirect(url_for("index"))

    return render_template("auth/login.html", title="Sign In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"Registered {form.user.data}.")
        return redirect(url_for("login"))
    return render_template("auth/register.html", title="Register", form=form)
