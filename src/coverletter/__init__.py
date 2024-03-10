import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


load_dotenv()


def init_db(app: Flask) -> None:
    """Initialise the database with the app context."""
    with app.app_context():
        db.init_app(app)
        db.create_all()


# @click.command("init-db")
# def init_db_command():
#     from flask import current_app

#     init_db(current_app)
#     click.echo("Initialized database.")


# def _init_app(app: Flask):
#     app.cli.add_command(init_db_command)


# create and configure the app
app = Flask(__name__, instance_relative_config=True)

from coverletter.config import Config

app.config.from_object(Config)

# load the instance config, if it exists, when not testing
app.config.from_prefixed_env("FLASK")

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path, exist_ok=True)
except OSError:
    pass


db = SQLAlchemy(app=app)

migrate = Migrate(app, db)

from coverletter import routes, db_models, auth

# from coverletter import auth

# app.register_blueprint(auth.bp)
