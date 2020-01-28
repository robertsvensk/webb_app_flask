from flask import Flask, render_template
import instagram

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/robert")
def robert():
    return "Hello, Robert!"

@app.route("/cathrine")
def cathrine():
    return "Tack så mycket Cathrine!"

if __name__ == "__main__":
    app.run(debug=True)
