"""
@ Author:  Javier Cienfuegos
@ Title:    ViewController.py
@ Description: Routes the url to multiple templates and basically
            controls the flow of web pages.
"""

from datetime import date
from flask import *
from flask_login import LoginManager, login_user, login_required, logout_user
from model import SQLDatabase, EmailLogManager, mongoDatabase
from user import User
from flask_mail import *
import logging, xmltodict, json


app = Flask(__name__)
app.secret_key = "ABAAMAMA"

# Email Management
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'cienfuegosjdevelop@gmail.com',
    MAIL_PASSWORD = 'Promagic1'
    )
mail = Mail(app)
emailmanager = EmailLogManager()
elogger = emailmanager.getEmailLogger()


# Login Management Objects
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login = "login"

# Database Management Objects
databaseType = "SQL" # You may choose 'MongoDB' or 'MySQL'
with open('cred.xml') as fd:
    if databaseType == "SQL":
        conn_cred = xmltodict.parse(fd.read())
        database = SQLDatabase(conn_cred=conn_cred)
    else:
        conn_cred = "mongodb://cienfuegosj:Promagic1!@assignmentorganizer-shard-00-00-jefyg.mongodb.net:27017,assignmentorganizer-shard-00-01-jefyg.mongodb.net:27017,assignmentorganizer-shard-00-02-jefyg.mongodb.net:27017/admin?replicaSet=assignmentorganizer-shard-0&ssl=true"
        database = mongoDatabase(conn_cred)

# View Routes


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Verify Credentials
        q = "SELECT * FROM user_account_info WHERE email='{0}' AND password='{1}'".format(email, password)
        results = database.query(q)

        if results is not None and len(results) != 0:
            usr = User(results[0]['UID'], results[0]['email'], results[0]['password'])
            login_user(usr)
            return redirect(url_for("user_dashboard", user=results[0]['UID']))
        else:
            return render_template("login.html", title="Home | Organizer", active="home", loginFailed=True)

    else:
        q = "SELECT * FROM user_account_info"
        results = database.query(q)
        invalidEmails = []
        if results is not None:
            for user_info in results:
                invalidEmails.append(user_info['email'])

        return render_template("login.html", title="Home | Organizer", active="home", loginFailed=False, invalidEmails=invalidEmails)


@app.route("/create_account", methods=["POST"])
def create_account():

    email = request.form['reg_email']
    password = request.form['pwd']
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    university = request.form['university']
    today_date = date.today()

    q = "INSERT INTO user_account_info(" \
        "firstname, lastname, password," \
        "email, avatar, date_registered," \
        "university) VALUES ('{0}', '{1}', '{2}', " \
        "'{3}', '{4}', '{5}', '{6}');".format(
        firstname, lastname, password, email, 0,
        str(today_date), university
    )

    print(database.insert(q))

    bSent = False
    try:
        msg = Message("Assignment Organizer: E-mail Confirmation",
                      sender="cienfuegosjdevelop@gmail.com",
                      recipients=[email])
        msg.html = render_template("confirmation_email.html", firstname=firstname)
        mail.send(msg)
        bSent = True
    except Exception as e:
        elogger.log(logging.INFO, "{0} Could not send confirmation e-mail to {1}.".format(date.today(), email))
        bSent = False
    finally:
        if bSent:
            elogger.log(logging.INFO, "{0}. Confirmation e-mail sent to {1}.".format(date.today(), email))

    return redirect(url_for('email_confirmation', successful=bSent))


@app.route("/email_confirmation/<successful>", methods=["GET"])
def email_confirmation(successful):
    return render_template("email_confirmation.html", successful=successful)


@login_manager.user_loader
def load_user(userid):
    q = "SELECT * FROM user_account_info WHERE UID='{0}'".format(userid)
    results = database.query(q)
    if results is not None:
        return User(userid, results[0]['email'], results[0]['password'])
    else:
        return None


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for('login'))


@app.route("/home/<user>", methods=["GET"])
@login_required
def user_dashboard(user):
    q1 = "SELECT * FROM user_pers_assignments WHERE userid = '{0}';".format(user)
    q2 = "SELECT * FROM team_assignments INNER JOIN team_members_map TM ON team_assignments.TAID = " \
        "TM.team_assignment_id WHERE TM.team_assignment_id = '{0}'".format(user)
    personal_assignments = database.query(q1)
    team_assignments = database.query(q2)
    return render_template("home.html", title="Assignment Organizer", active="home", personal_assignments=personal_assignments, team_assignments=team_assignments)


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