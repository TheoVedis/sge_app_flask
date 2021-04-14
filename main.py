from flask import Flask, render_template, request, redirect, url_for, Markup, session
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json
from package.login_manager import check_password, is_logged, msg_feedback
from package.utility import random_secret_key

app = Flask(
    __name__, static_folder="./assets/static/", template_folder="./assets/templates/"
)

app.secret_key = random_secret_key(10)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    """Documentation
    Redirige les utilisateurs
        soit vers la page de login
        soit vers le dashboard.

    Parametre:
        path: chemin d'acces au site

    Sortie:
        le template de la page a afficher ou une redirection
    """
    if path != "":
        return redirect(url_for("index"))

    if not is_logged(session):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html", banner=Markup(render_template("banner.html"))
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    """Documentation
    Gere les connexions des utilisateurs

    Sortie:
        page de connexion, redirection ou message d'erreur
    """
    error = None

    if is_logged(session):
        return redirect(url_for("index"))

    if request.method == "POST":
        # Acces via le bouton du formulaire de connexion
        username = request.form["username"]
        password = request.form["password"]

        print("ID:", username, "/", password)

        succes = check_password(username, password)
        error = msg_feedback(succes)

        if succes == 0:
            session["is_logged"] = True
            session["username"] = username
            return redirect(url_for("index"))

        return render_template(
            "login.html", banner=Markup(render_template("banner.html")), error=error
        )

    return render_template(
        "login.html", banner=Markup(render_template("banner.html")), error=None
    )


if __name__ == "__main__":
    app.run(debug=True)
