from flask import Flask, render_template, request, redirect, url_for
import instagram

app = Flask(__name__)

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

LoggedOn = False
# Login handling

@app.route("/")
def home():
    return render_template("home.html", Login = LoggedOn)

@app.route("/about")
def about():
    return render_template("about.html", Login = LoggedOn)

@app.route("/login", methods=['GET', 'POST'])
def login():
    global LoggedOn
    if request.method == "POST":
        LoggedOn = True
        return redirect(url_for("home"))
    return render_template("login.html", Login = LoggedOn)

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

if __name__ == "__main__":
    waterPlants()
    app.run(debug=True)
