import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user


load_dotenv()

app = Flask(__name__, instance_relative_config=True)

# create and configure the app
from coverletter.config import Config

app.config.from_object(Config)

# load the instance config, if it exists, when not testing
app.config.from_prefixed_env("FLASK")

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path, exist_ok=True)
except OSError:
    pass

login = LoginManager(app)
login.login_view = "login"

db = SQLAlchemy(app=app)

migrate = Migrate(app, db)

from coverletter import db_models
from coverletter.views import *

# from coverletter import auth

# app.register_blueprint(auth.bp)


@app.shell_context_processor
def make_shell_context() -> dict:
    import sqlalchemy as sa
    import sqlalchemy.orm as so

    return {"sa": sa, "so": so, "db": db, "User": db_models.User, "Resume": db_models.Resume}


@app.cli.command("init-db")
def init_db_command():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
