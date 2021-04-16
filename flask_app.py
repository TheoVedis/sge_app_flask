import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ClientsideFunction, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask, Markup, redirect, render_template, request, session, url_for

from package.data_base_manager import get_data, get_id_cpt
from package.login_manager import check_password, is_logged, msg_feedback
from package.utility import dash_kwarg, graph, random_secret_key

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
    print("Hey INDEX")

    # if path != "":
    #     return redirect(url_for(".index"))

    if not is_logged(session):
        return redirect(url_for(".login"))

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


########################################################################
#                                 DASH                                 #
########################################################################


dash_app = dash.Dash(__name__, server=app, url_base_pathname="/dashboard/")

head = html.Div(
    id="head",
    children=[
        # Represente l'url
        dcc.Location(id="url", refresh=True),
        # Represente le stockage de variable de session
        dcc.Store(id="session", storage_type="session"),
        # Banniere
        html.Div(
            children=[
                html.H2("SGE_APP"),
                html.Button(id="disconnect-btn", children=["deconnecter"], n_clicks=0),
                html.Img(src="./assets/static/img/stock-icon.png"),
            ],
            className="banner",
        ),
    ],
)

layout_main = html.Div(
    id="page-content",
    children=[
        html.Button(
            id="sideMenu-btn",
            children=[
                html.Img(src="./assets/static/img/right_arrow.png", width=30),
                html.Img(src="./assets/static/img/right_arrow_green.png", width=30),
            ],
        ),
        html.Div(
            id="sideMenu",
            className="sidenav",
            hidden=False,
            children=[
                html.P(className="title", children=["FILTRE"]),
                html.Div(
                    className="filtre",
                    children=[
                        dcc.Dropdown(id="select-id_cpt", multi=True),
                        dcc.DatePickerRange(
                            id="date-range-picker",
                            className="datePicker",
                            display_format="DD/MM/YYYY",
                        ),
                        html.Button(id="filtre-valid", children="valid"),
                    ],
                ),
            ],
        ),
        html.Div(id="dashboard", children=[dcc.Graph(id="graph", figure={})]),
    ],
)


dash_app.layout = html.Div(children=[head, layout_main])

outputs = [
    Output("url", "pathname"),
    Output("select-id_cpt", "options"),
    Output("graph", "figure"),
]
inputs = [Input("disconnect-btn", "n_clicks"), Input("filtre-valid", "n_clicks")]
states = [
    State("select-id_cpt", "value"),
    State("date-range-picker", "end_date"),
    State("date-range-picker", "start_date"),
]


@dash_app.callback(outputs, inputs, states)
@dash_kwarg(outputs, inputs, states)
def dashboard_manager(outputs, inputs, trigger):
    """Documentation
    Gestionnaire principal des callbacks pour le tableau de bord.
    Avec les declencheurs (trigger)

    Parametre:
        outputs: Dictionnaire des variables de sortie initialisé a la valeur dash.no_update
            format ouputs[component_id][component_property]
        inputs: Dictionnaire des variables d'entrée (déclencheur (trigger) et les statiques (states)) avec leur valeur
            format inputs[component_id][component_property]
        trigger: Dictionnaire du composant déclencheur
            trigger["id"] => component_id.component_property ex: "url.pathname"
            trigger["value"] => valeur du composant ex: '/login'

    Sortie:
        outputs: Avec des variables modifiées ou des dash.no_update (par defaut)
    """
    print("TRIGGER:", trigger)

    # Quand la page charge
    if trigger["id"] == ".":
        # Si pas connecter on le renvoie a la page de connexion
        if not is_logged(session):
            outputs["url"]["pathname"] = "/login"
            return outputs

        # recupération des id_cpt pour le selecteur
        outputs["select-id_cpt"]["options"] = [
            {"label": i, "value": i} for i in get_id_cpt()
        ]

        return outputs

    if trigger["id"] == "disconnect-btn.n_clicks":
        return disconnect(outputs, inputs)

    if trigger["id"] == "filtre-valid.n_clicks":
        # TODO le graph
        outputs["graph"]["figure"] = graph(
            inputs["select-id_cpt"]["value"],
            inputs["date-range-picker"]["start_date"],
            inputs["date-range-picker"]["end_date"],
        )

    return outputs


def disconnect(outputs, inputs):
    """Documentation
    Deconnect l'utilisteurs, clear les variables de session ect..
    """
    if inputs["disconnect-btn"]["n_clicks"] == 0:
        raise PreventUpdate

    # TODO l'action de la deconnexion
    # Redirection
    outputs["url"]["pathname"] = "/login"
    session["is_logged"] = False
    return outputs


dash_app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="openNav"),
    Output("sideMenu", "hidden"),
    Input("sideMenu-btn", "n_clicks"),
)

if __name__ == "__main__":
    dash_app.enable_dev_tools(debug=True)
    app.run(debug=True)
