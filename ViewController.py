"""
@ Author:  Javier Cienfuegos
@ Title:    ViewController.py
@ Description: Routes the url to multiple templates and basically
            controls the flow of web pages.
"""

from flask import *
from flask_login import *
from model import Database
from user import User
import logging, xmltodict, json


app = Flask(__name__)

# Login Management Objects
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login = "login"

# Database Management Objects
with open('cred.xml') as fd:
    conn_cred = xmltodict.parse(fd.read())
database = Database(conn_cred=conn_cred)


# View Routes
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Verify Credentials
        q = "SELECT * FROM user_account_info WHERE username='{0}' AND password='{1}'".format(username, password)
        results = database.query(q)

        if results is not None:
            usr = User(results[0]['UID'], results[0]['username'], results[0]['password'])
            login_user(usr)
            return redirect(url_for("user_home"))
        else:
            return render_template("login.html", title="Home | Organizer", active="home", loginFailed=True)

    else:
        return render_template("login.html", title="Home | Organizer", active="home", loginFailed=False)


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("loginpage"))


@app.route("/home", methods=["GET"])
@login_required
def user_home():
    return render_template("user_home.html", title="Assignment Organizer", active="home")


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