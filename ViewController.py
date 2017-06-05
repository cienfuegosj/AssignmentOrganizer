"""
@ Author:  Javier Cienfuegos
@ Title:    ViewController.py
@ Description: Routes the url to multiple templates and basically
            controls the flow of web pages.
"""

from flask import *
from flask_login import *
from Model import Database
from User import User
import logging


app = Flask(__name__)

# Login Management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login = "login"

# Database Management


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        # Validate Credentials
    else:
        return render_template("index.html", title="Login | Organizer")

if __name__ == '__main__':
    app.run(debug=True)