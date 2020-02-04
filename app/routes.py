from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from app.plant import startWatering

####################### TEMP LOGIN ##########################
LoggedOn = False
class User():
    name = ''
admin = User()
admin.name = 'Robert'
user = admin

####################### LOGIN ROUTES ##############################
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

#################### MAIN MENY ROUTES ######################
@app.route("/")
def home():
    global user
    return render_template("home.html", Login = LoggedOn, user = user)

@app.route("/about")
def about():
    return render_template("about.html", Login = LoggedOn)

@app.route("/forum")
def forum():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author': {'username': 'Cathrine'},
            'body': 'Lady Bird is an awesome movie!'
        }
    ]
    return render_template("forum.html", title='Forum', posts=posts)

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

################# HIDDEN ROUTES ################################
@app.route("/robert")
def robert():
    return "Hello, Robert!"

@app.route("/cathrine")
def cathrine():
    return "Tack så mycket Cathrine!"
