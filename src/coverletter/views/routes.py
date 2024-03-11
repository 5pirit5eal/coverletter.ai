"""For explanation of the code, see the following links:
https://flask.palletsprojects.com/en/3.0.x/tutorial/views/
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
"""

from coverletter import app
from flask_login import login_required
from flask import render_template


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("home/index.html", title="Home")
