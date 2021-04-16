from typing import List
from flask import Flask, render_template, request, redirect, url_for, Markup, session
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import pandas as pd
import numpy as np
import datetime
import json
from package.login_manager import check_password, is_logged, msg_feedback
from package.utility import graph, random_secret_key
from package.data_base_manager import get_id_cpt

app = Flask(
    __name__, static_folder="./assets/static/", template_folder="./assets/templates/"
)

app.secret_key = random_secret_key(123)


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
    session["test"] = "TESTEUX"
    print(session)
    if path != "":
        return redirect(url_for("index"))

    if not is_logged(session):
        return redirect(url_for("login"))

    return redirect("/dashboard")


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


dash_app = dash.Dash(__name__, server=app, url_base_pathname="/dashboard/")

dash_app.layout = html.Div(
    children=[
        dcc.Store(id="session"),
        "Dash app 1",
        html.H1(id="test1", children=[]),
        html.Button(id="test2", n_clicks=0),
    ]
)


# Use the same session var work
@dash_app.callback(Output("test1", "children"), Input("test2", "n_clicks"))
def test(n_clicks):
    print(n_clicks)
    print(session)

    return ["OK"]


if __name__ == "__main__":
    app.run(debug=True)
