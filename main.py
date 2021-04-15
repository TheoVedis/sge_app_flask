from typing import List
from flask import Flask, render_template, request, redirect, url_for, Markup, session

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

    return dashboard()


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


def dashboard():

    id_cpt: str = "".join(
        ['<option value="{}">{}</option>'.format(i, i) for i in get_id_cpt()]
    )

    return render_template(
        "dashboard.html",
        banner=Markup(render_template("banner.html")),
        id_cpt=Markup(id_cpt),
    )


@app.route("/applyFiltre", methods=["POST"])
def applyFiltre():
    # recupération des données
    data = request.get_json()

    id_cpt: List[str] = data["value"]

    # Format datetime ou str avoir avec la BD
    start_date: datetime.datetime = datetime.datetime.strptime(
        data["startDate"], "%d-%m-%Y"
    )
    end_date: datetime.datetime = datetime.datetime.strptime(
        data["endDate"], "%d-%m-%Y"
    )

    plot = graph(id_cpt, start_date, end_date)

    print(plot)
    print("APPLY")
    # 01/09/2008 - 01/10/2008
    return json.dumps({"success": True, "plot": plot})


if __name__ == "__main__":
    app.run(debug=True)
