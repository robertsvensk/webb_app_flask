from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/robert")
def robert():
    return "Hello, Robert!"

@app.route("/cathrine")
def cathrine():
    return "Tack så mycket Cathrine!"

if __name__ == "__main__":
    app.run(debug=True)
