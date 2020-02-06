#----------------------- LIB ----------------------#
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

#------------------------ APP ---------------------#
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.plant import startWatering
from app.models import User

####################### LOGIN ROUTES ##############################
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        # Check user against database
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        # Next page handling
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template("login.html", title='Sign In', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

#################### MAIN MENY ROUTES ######################
@app.route("/")
def home():
    global user
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/forum")
@login_required
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

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}
        ]
    return render_template('user.html', user=user, posts=posts)


########################### WATERING APP ############################
ButtonPressed = 0
@app.route("/plants", methods=['GET', 'POST'])
@login_required
def plants():
    global ButtonPressed
    if request.method == "POST":
        ButtonPressed += 1
        return(redirect(url_for("water")))
    return render_template("plants.html", Button = ButtonPressed)

@app.route("/water")
@login_required
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
