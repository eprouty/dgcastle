from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link

from dgcastle import dgcastle

app = Flask(__name__)
Bootstrap(app)

nav = Nav()
nav.register_element('top', Navbar(
    View('DGCastle', '.home'),
    Subgroup('Import',
        View('Challonge', '.challonge')
    )
))
nav.init_app(app)

DGCastle = dgcastle.DGCastle()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/challonge")
@app.route("/challonge/<tournament>")
def challonge(tournament=None):
    if tournament:
        # Need to make a call to DGCastle to import this tournament information
        info = DGCastle.challonge_import(tournament)
        return render_template("challonge.html", info=info)
    else:
        return render_template("challonge.html")

if __name__ == "__main__":
    app.run()