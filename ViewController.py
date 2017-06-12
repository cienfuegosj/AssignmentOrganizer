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
import logging, xmltodict


app = Flask(__name__)

# Login Management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login = "login"

# Database Management
with open('cred.xml') as fd:
    conn_cred = xmltodict.parse(fd.read())
database = Database(conn_cred=conn_cred)


# View Routes
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        # Validate Credentials

    else:
        return render_template("login.html", title="Home | Organizer",
                               active='home')


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html", title="About | Organizer")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", title="Contact | Organizer")
    else:
        # Do any email contact things here
        pass

if __name__ == '__main__':
    app.run(debug=True)