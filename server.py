from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from dgcastle import dgcastle

app = Flask(__name__)
Bootstrap(app)

DGCastle = dgcastle.DGCastle()

@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run()