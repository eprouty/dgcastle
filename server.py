from flask import Flask

from dgcastle import dgcastle

app = Flask(__name__)

DGCastle = dgcastle.DGCastle()

@app.route("/")
def home():
    return "Hello, Disc Golfers!"

if __name__ == "__main__":
    app.run()