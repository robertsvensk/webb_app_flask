from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from forms import LoginForm
import instagram

######################## INIT ###############################
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

####################### WATER ###############################
WaterPlants = False
def startWatering():
    global WaterPlants
    WaterPlants = True

def waterPlants():
    global WaterPlants
    if (WaterPlants):
        timer = 1000
        while (timer > 0):
            print(timer)
        WaterPlants = False

####################### LOGIN ###############################
LoggedOn = False
class User():
    name = ''

admin = User()
admin.name = 'Robert'
user = admin

####################### ROUTES ##############################
@app.route("/")
def home():
    global user
    return render_template("home.html", Login = LoggedOn, user = user)

@app.route("/about")
def about():
    return render_template("about.html", Login = LoggedOn)

@app.route("/login", methods=['GET', 'POST'])
def login():
    global LoggedOn
    form = LoginForm()
    if form.validate_on_submit():
        LoggedOn = True
        flash('Login requested for user {}, rembember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for("home"))
    return render_template("login.html", title='Sign In', form=form)

@app.route("/logout")
def logout():
    global LoggedOn
    LoggedOn = False
    return redirect(url_for("home"))

ButtonPressed = 0
@app.route("/plants", methods=['GET', 'POST'])
def plants():
    global ButtonPressed
    if request.method == "POST":
        ButtonPressed += 1
        return(redirect(url_for("water")))
    return render_template("plants.html", Button = ButtonPressed, Login = LoggedOn)

@app.route("/water")
def water():
    startWatering()
    return(redirect(url_for('plants')))

@app.route("/robert")
def robert():
    return "Hello, Robert!"

@app.route("/cathrine")
def cathrine():
    return "Tack så mycket Cathrine!"

############################# MAIN ############################
if __name__ == "__main__":
    #Thread the program so that app is handle by one thread and watering handled by another.
    app.run(debug=True)
    waterPlants()
