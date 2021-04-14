from flask import Flask, render_template, request, redirect, url_for, Markup
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json


app = Flask(
    __name__, static_folder="./assets/static/", template_folder="./assets/templates/"
)
app.secret_key = "AECVSBQNKOIUFHAN"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        print(user, password)

        return redirect(url_for("index"))

    else:
        return render_template(
            "login.html", banner=Markup(render_template("banner.html"))
        )


if __name__ == "__main__":
    app.run(debug=True)
