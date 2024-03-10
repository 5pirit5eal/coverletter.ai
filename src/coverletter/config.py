import os
from coverletter import app


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = (
        f"{os.getenv('DATABASE_TYPE', 'sqlite+pysqlite')}:"
        f"///{os.path.join(app.instance_path, 'coverletter.db')}"
    )
