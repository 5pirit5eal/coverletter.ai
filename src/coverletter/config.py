import os
from coverletter import app
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = (
        f"{os.getenv('DATABASE_TYPE', 'sqlite+pysqlite')}:"
        f"///{os.path.join(app.instance_path, 'coverletter.db')}"
    )
