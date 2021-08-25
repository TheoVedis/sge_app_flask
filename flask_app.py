import datetime
from typing import Any, Dict

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from flask_login.utils import login_user
import pandas as pd
from dash.dependencies import ClientsideFunction, Input, Output, State
from dash.exceptions import PreventUpdate
from dash_core_components import Dropdown
from dash_html_components import Div
from flask import Flask, Markup, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, logout_user, current_user

from package.data_base_manager import (
    get_batiment,
    get_client,
    get_conso,
    get_data,
    get_facturation_date,
    get_groupe,
    get_id_cpt,
    get_type_energie,
)
from package.login_manager import User, check_password, is_logged, msg_feedback
from package.utility import (
    dash_kwarg,
    graph,
    is_facturation_date,
    random_secret_key,
    table,
)

app = Flask(
    __name__, static_folder="./assets/static/", template_folder="./assets/templates/"
)

app.secret_key = random_secret_key(123)
login_manager = LoginManager(app)
current_user: User = current_user


@login_manager.user_loader
def load_user(user_id):
    return User.get_user(user_id)


@login_manager.unauthorized_handler
def unauthorized_route():
    return index()


# @app.route("/", defaults={"path": ""})
# @app.route("/<path:path>")
def index(path: str = None):
    """Documentation
    Redirige les utilisateurs
        soit vers la page de login
        soit vers le dashboard.

    Parametre:
        path: chemin d'acces au site

    Sortie:
        le template de la page a afficher ou une redirection
    """

    if not is_logged(current_user):
        return redirect(url_for(".login"))

    return redirect("/dashboard")


@app.errorhandler(404)
def test_error(err):
    """Documentation
    Déclenché en cas de page non trouvée, redirige automatiquement a l'index
    """
    return index()


@app.route("/login", methods=["POST", "GET"])
def login():
    """Documentation
    Gere les connexions des utilisateurs

    Sortie:
        page de connexion, redirection ou message d'erreur
    """
    error = None

    #### TODO Enlever l'auto log
    # print("############### A ENLEVER ################### - Auto log")
    # session["is_logged"] = True
    # session["username"] = "test"
    ############################

    if is_logged(current_user):
        return index()

    if request.method == "POST":
        # Acces via le bouton du formulaire de connexion
        username: str = request.form["username"]
        password: str = request.form["password"]

        print("ID:", username, "/", password)

        succes = check_password(username, password)

        if succes == 0:
            # session["is_logged"] = True
            # session["username"] = username
            user = User.get_user(username)
            login_user(user, remember=False)
            return index()

        error = msg_feedback(succes)

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

# Ajout de l'authentification sur la partie dash
for view_func in app.view_functions:
    if view_func.startswith("/dashboard/"):
        app.view_functions[view_func] = login_required(app.view_functions[view_func])

head = html.Div(
    id="head",
    children=[
        # Represente l'url
        dcc.Location(id="url", refresh=True),
        # Banniere
        html.Div(
            children=[
                html.H2("SGE_APP"),
                html.Div(
                    id="head-content",
                    children=[
                        html.Span(id="head-msg", children="Bienvenue ..."),
                        html.Button(
                            id="disconnect-btn", children=["deconnecter"], n_clicks=0
                        ),
                    ],
                ),
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
                        dcc.Dropdown(
                            id="select-groupe",
                            multi=False,
                            placeholder="Select groupe...",
                            value=None,
                        ),
                        dcc.Dropdown(
                            id="select-client",
                            multi=False,
                            placeholder="Select client...",
                            value=None,
                        ),
                        dcc.Dropdown(
                            id="select-type",
                            multi=False,
                            placeholder="Select type d'energie...",
                        ),
                        dcc.Dropdown(
                            id="select-bat",
                            multi=False,
                            placeholder="Select batiment...",
                        ),
                        dcc.Dropdown(
                            id="select-id_cpt",
                            multi=False,
                            placeholder="Select compteur...",
                        ),  # multi=False signifie un seul compteur selectionnable a la fois
                        dcc.Dropdown(
                            id="select-periode",
                            multi=False,
                            style={"display": "None"},
                            options=[
                                {"label": "Jour", "value": "jour"},
                                {"label": "Mois", "value": "mois"},
                                {"label": "Trimestre", "value": "trim"},
                                {"label": "SGE Facturation", "value": "sge"},
                            ],
                            value="jour",
                            searchable=False,
                        ),
                        dcc.DatePickerRange(
                            id="date-range-picker",
                            className="datePicker",
                            display_format="DD/MM/YYYY",
                            first_day_of_week=1,
                        ),
                        html.Button(id="filtre-valid", children="valider"),
                        html.P(
                            id="warning-date-facturation",
                            children="⚠ Les dates choisies ne sont pas des dates de facturation !",
                            style={"margin": "1%", "color": "red", "display": "block"},
                        ),
                        html.P(className="title", children=["Date Facturation"]),
                        html.Div(
                            children=[
                                html.H4(children="Date de début"),
                                dcc.Dropdown(
                                    id="date-facturation-start-annee",
                                    multi=False,
                                    placeholder="Annee",
                                    value=None,
                                ),
                                dcc.Dropdown(
                                    id="date-facturation-start-mois",
                                    multi=False,
                                    placeholder="Mois",
                                    value=None,
                                ),
                                dcc.Dropdown(
                                    id="date-facturation-start-jour",
                                    multi=False,
                                    placeholder="Jour",
                                    value=None,
                                ),
                            ],
                        ),
                        html.Div(
                            children=[
                                html.H4(children="Date de fin"),
                                dcc.Dropdown(
                                    id="date-facturation-end-annee",
                                    multi=False,
                                    placeholder="Annee",
                                    value=None,
                                ),
                                dcc.Dropdown(
                                    id="date-facturation-end-mois",
                                    multi=False,
                                    placeholder="Mois",
                                    value=None,
                                ),
                                dcc.Dropdown(
                                    id="date-facturation-end-jour",
                                    multi=False,
                                    placeholder="Jour",
                                    value=None,
                                ),
                            ],
                        ),
                        # Sert a rallonger le menu des filtres pour s'adapter a des écrans plus petit
                        html.H4(
                            children="",
                            style={
                                "padding-top": "100%",
                                "display": "block",
                            },
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="dashboard",
            children=[
                dcc.Tabs(
                    id="tabs",
                    value="tab1",
                    children=[
                        dcc.Tab(
                            label="Valeur Index",
                            value="tab1",
                            children=[
                                dcc.Graph(id="graph", figure={}),
                                dt.DataTable(
                                    id="table",
                                    # columns=[{"name": i, "id": i} for i in data.columns],
                                    # data=data.to_dict("records"),
                                    export_format="csv",
                                    sort_action="native",
                                    # filter_action="native",
                                    # filter_query="",
                                    style_as_list_view=True,
                                    style_cell={"padding": "5px"},
                                    style_header={
                                        "backgroundColor": "rgb(230, 230, 230)",
                                        "fontWeight": "bold",
                                    },
                                    # style_data_conditional=[  # mettre en valeur les pts anormaux
                                    #     {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"},
                                    #     {
                                    #         "if": {
                                    #             "filter_query": "{Value} > 6317498",
                                    #             "column_id": "Value",
                                    #         },
                                    #         "backgroundColor": "tomato",
                                    #         "color": "white",
                                    #     },
                                    # ],
                                    page_size=30,
                                    row_selectable="multi",
                                    style_header_conditional=[
                                        # {
                                        #     "if": {"column_id": "Index"},
                                        #     "display": "None",
                                        # }
                                    ],
                                    style_data_conditional=[
                                        # Probleme cacher la colonne index décale les filtres
                                        # {
                                        #     "if": {"column_id": "Index"},
                                        #     "display": "None",
                                        # }
                                    ],
                                ),
                            ],
                        ),
                        dcc.Tab(
                            label="Consomation",
                            value="tab2",
                            children=[
                                dcc.Graph(id="graph2", figure={}),
                                dt.DataTable(
                                    id="table2",
                                    export_format="csv",
                                    sort_action="native",
                                    # filter_action="native",
                                    style_as_list_view=True,
                                    style_cell={"padding": "5px"},
                                    style_header={
                                        "backgroundColor": "rgb(230, 230, 230)",
                                        "fontWeight": "bold",
                                    },
                                    page_size=30,
                                    row_selectable="multi",
                                    style_header_conditional=[
                                        # {
                                        #     "if": {"column_id": "Index"},
                                        #     "display": "None",
                                        # }
                                    ],
                                    style_data_conditional=[
                                        # Probleme cacher la colonne index décale les filtres
                                        # {
                                        #     "if": {"column_id": "Index"},
                                        #     "display": "None",
                                        # }
                                    ],
                                ),
                            ],
                        ),
                        dcc.Tab(
                            label="Information",
                            value="tab3",
                            children=["Hey la page 3"],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


dash_app.layout = html.Div(children=[head, layout_main])

facturation_date = get_facturation_date()

# Important ordonner les outputs par compononent ID
outputs = [
    Output("url", "pathname"),
    Output("head-msg", "children"),
    # Selecteur (Filtre)
    Output("select-groupe", "options"),
    Output("select-groupe", "style"),  # Cacher groupe
    Output("select-client", "options"),
    Output("select-client", "style"),  # Cacher client
    Output("select-type", "options"),
    Output("select-bat", "options"),
    Output("select-id_cpt", "options"),
    # Date range par defaut
    Output("date-range-picker", "start_date"),
    Output("date-range-picker", "end_date"),
    # Date facturation
    Output("date-facturation-start-annee", "options"),
    Output("date-facturation-start-mois", "options"),
    Output("date-facturation-start-jour", "options"),
    Output("date-facturation-end-annee", "options"),
    Output("date-facturation-end-mois", "options"),
    Output("date-facturation-end-jour", "options"),
    # Afficher / cacher les filtres en fonction de l'onglet
    Output("select-periode", "style"),
    ############# Tab1 #############
    Output("graph", "figure"),
    Output("table", "style_data_conditional"),
    Output("table", "columns"),
    Output("table", "data"),
    Output("table", "style_data"),
    Output("table", "filter_action"),
    Output("table", "filter_query"),
    ############# Tab2 #############
    Output("graph2", "figure"),
    Output("table2", "style_data_conditional"),
    Output("table2", "columns"),
    Output("table2", "data"),
    Output("table2", "style_data"),
    Output("table2", "filter_action"),
    Output("table2", "filter_query"),
    # warning-date-facturation
    Output("warning-date-facturation", "style"),
]
inputs = [
    Input("disconnect-btn", "n_clicks"),
    Input("filtre-valid", "n_clicks"),
    Input("graph", "selectedData"),
    Input("tabs", "value"),
    Input("graph2", "selectedData"),
    Input("select-groupe", "value"),
    Input("select-client", "value"),
    Input("select-type", "value"),
    Input("select-bat", "value"),
    Input("select-id_cpt", "value"),
    # Actualisation du message warning-date-facturation
    Input("date-range-picker", "end_date"),
    Input("date-range-picker", "start_date"),
    # Trigger selection date de facturation
    Input("date-facturation-start-annee", "value"),
    Input("date-facturation-start-mois", "value"),
    Input("date-facturation-start-jour", "value"),
    Input("date-facturation-end-annee", "value"),
    Input("date-facturation-end-mois", "value"),
    Input("date-facturation-end-jour", "value"),
]
states = [
    State("select-periode", "value"),
    State("table", "data"),
    State("table", "filter_query"),
    State("table2", "data"),
    State("table2", "filter_query"),
    State("warning-date-facturation", "style"),
]


@dash_app.callback(outputs, inputs, states)
@dash_kwarg(outputs, inputs, states)
def dashboard_manager(
    outputs: Dict[str, Dict[str, Any]],
    inputs: Dict[str, Dict[str, Any]],
    trigger: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
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

    # Si pas connecter on le renvoie a la page de connexion
    if not is_logged(current_user):
        outputs["url"]["pathname"] = "/login"
        return outputs

    # Quand la page charge
    if trigger["id"] == ".":

        outputs["head-msg"]["children"] = "Bienvenue " + str(current_user.username)

        client = None
        if not current_user.is_admin():
            client = current_user.name
            # Affichage des selecteur SGE
            outputs["select-groupe"]["style"] = {"display": "None"}
            outputs["select-client"]["style"] = {"display": "None"}
        else:
            # récupération des groupes pour le selecteur
            outputs["select-groupe"]["options"] = value_to_dropdown(get_groupe())

            # récupération des noms des clients pour le selecteur
            outputs["select-client"]["options"] = value_to_dropdown(get_client())

        # recupération des id_cpt pour le selecteur
        outputs["select-id_cpt"]["options"] = value_to_dropdown(
            get_id_cpt(client=client)
        )

        # récupération des types d'energie pour le selecteur
        outputs["select-type"]["options"] = value_to_dropdown(get_type_energie())

        # récupération des batiments pour le selecteur
        outputs["select-bat"]["options"] = value_to_dropdown(
            get_batiment(name_client=client)
        )

        # Update date de facturation dropdow
        date_facturation: pd.DataFrame = get_facturation_date()
        outputs["date-facturation-start-annee"]["options"] = value_to_dropdown(
            set(date_facturation["Annee"].values)
        )

        outputs["date-facturation-end-annee"]["options"] = value_to_dropdown(
            set(date_facturation["Annee"].values)
        )

        # TODO A REMETTRE UNE FOIS LES TESTS FINI
        # Date par defaut debut d'année a aujourd'hui
        # outputs["date-range-picker"]["end_date"] = datetime.datetime.today().strftime(
        #     "%Y-%m-%d"
        # )
        # outputs["date-range-picker"]["start_date"] = datetime.datetime.today().strftime(
        #     "%Y-01-01"
        # )

        # TODO A ENLEVER UNE FOIS LES TESTS FINI
        outputs["date-range-picker"]["end_date"] = "2008-09-01"
        outputs["date-range-picker"]["start_date"] = "2008-08-01"

        return outputs

    # Bouton deconnecter
    if trigger["id"] == "disconnect-btn.n_clicks":
        return disconnect(outputs, inputs)

    # Bouton validation des filtres
    if trigger["id"] == "filtre-valid.n_clicks":
        return valid_filter(outputs, inputs)

    # Mise en evidence des points selectionner sur le graph valeur index
    if trigger["id"] == "graph.selectedData":
        return highlight_point(outputs, inputs, "graph", "table")

    # Mise en evidence des points selectionner sur le graph2 consommation
    if trigger["id"] == "graph2.selectedData":
        return highlight_point(outputs, inputs, "graph2", "table2")

    # Changement de tabs
    if trigger["id"] == "tabs.value":
        return change_tab(outputs, inputs, trigger["value"])

    if trigger["id"] == "select-groupe.value":
        # si l'utilisateur n'est pas admin, il ne peut pas selectionner de groupe
        if not current_user.is_admin():
            raise PreventUpdate

        outputs["select-client"]["options"] = value_to_dropdown(
            get_client(groupe=trigger["value"])
        )

        outputs["select-bat"]["options"] = value_to_dropdown(
            get_batiment(
                group=trigger["value"], name_client=inputs["select-client"]["value"]
            )
        )

        outputs["select-id_cpt"]["options"] = value_to_dropdown(
            get_id_cpt(
                group=trigger["value"],
                type_energie=inputs["select-type"]["value"],
                client=inputs["select-client"]["value"],
                name_bat=inputs["select-bat"]["value"],
            )
        )

        return outputs

    # Selection d'un client
    if trigger["id"] == "select-client.value":
        # si l'utilisateur n'est pas admin il ne peut pas selectionner de client
        if not current_user.is_admin():
            raise PreventUpdate

        # récupération des batiments pour le selecteur
        outputs["select-bat"]["options"] = value_to_dropdown(
            get_batiment(
                name_client=trigger["value"], group=inputs["select-groupe"]["value"]
            )
        )

        # Récupération des id_cpt pour le selecteur
        outputs["select-id_cpt"]["options"] = value_to_dropdown(
            get_id_cpt(
                client=inputs["select-client"]["value"],
                name_bat=inputs["select-bat"]["value"],
                type_energie=inputs["select-type"]["value"],
            )
        )

        return outputs

    # Selection d'un type d'energie
    if trigger["id"] == "select-type.value":
        client = inputs["select-client"]["value"]

        if not current_user.is_admin():
            client = current_user.name

        # récupération des batiments pour le selecteur
        # outputs["select-bat"]["options"] = value_to_dropdown(
        #     get_batiment(
        #         type_energie=trigger["value"],
        #         name_client=inputs["select-client"]["value"],
        #     )
        # )

        # Récupération des id_cpt pour le selecteur
        outputs["select-id_cpt"]["options"] = value_to_dropdown(
            get_id_cpt(
                client=client,
                name_bat=inputs["select-bat"]["value"],
                type_energie=inputs["select-type"]["value"],
            )
        )

        return outputs

    # Selection d'un batiment
    if trigger["id"] == "select-bat.value":
        client = inputs["select-client"]["value"]

        if not current_user.is_admin():
            client = current_user.name

        # Récupération des id_cpt pour le selecteur
        outputs["select-id_cpt"]["options"] = value_to_dropdown(
            get_id_cpt(
                client=client,
                name_bat=inputs["select-bat"]["value"],
                type_energie=inputs["select-type"]["value"],
            )
        )

        return outputs

    # Selection d'un compteur
    if trigger["id"] == "select-id_cpt.value":
        if trigger["value"] is not None and not trigger["value"] == []:
            # TODO update les autres filtres
            pass
        raise PreventUpdate

    # Acualisation du message warning-date-facturation
    if trigger["id"] == "date-range-picker.start_date":
        return hide_date_warning(
            outputs,
            inputs,
            display=(
                not is_facturation_date(inputs["date-range-picker"]["end_date"])
                or not is_facturation_date(inputs["date-range-picker"]["start_date"])
            ),
        )

    if trigger["id"] == "date-range-picker.end_date":
        return hide_date_warning(
            outputs,
            inputs,
            display=(
                not is_facturation_date(inputs["date-range-picker"]["end_date"])
                or not is_facturation_date(inputs["date-range-picker"]["start_date"])
            ),
        )

    # Selection date de facturation
    if trigger["id"] == "date-facturation-start-annee.value":
        date_facturation: pd.DataFrame = get_facturation_date()
        outputs["date-facturation-start-mois"]["options"] = value_to_dropdown(
            date_facturation[date_facturation["Annee"] == trigger["value"]][
                "Mois"
            ].values
        )

        return outputs

    if trigger["id"] == "date-facturation-start-mois.value":
        date_facturation: pd.DataFrame = get_facturation_date()

        year_date = date_facturation[
            date_facturation["Annee"] == inputs["date-facturation-start-annee"]["value"]
        ]

        outputs["date-facturation-start-jour"]["options"] = value_to_dropdown(
            year_date[year_date["Mois"] == trigger["value"]]["Jour"].values
        )

        return outputs

    if trigger["id"] == "date-facturation-start-jour.value":
        date_facturation: pd.DataFrame = get_facturation_date()

        year: str = str(inputs["date-facturation-start-annee"]["value"])
        month: str = str(inputs["date-facturation-start-mois"]["value"])
        day: str = str(trigger["value"])

        outputs["date-range-picker"]["start_date"] = "-".join([year, month, day])
        outputs = hide_date_warning(
            outputs,
            inputs,
            display=not is_facturation_date(inputs["date-range-picker"]["end_date"]),
        )
        return outputs

    if trigger["id"] == "date-facturation-end-annee.value":
        date_facturation: pd.DataFrame = get_facturation_date()
        outputs["date-facturation-end-mois"]["options"] = value_to_dropdown(
            date_facturation[date_facturation["Annee"] == trigger["value"]][
                "Mois"
            ].values
        )

        return outputs

    if trigger["id"] == "date-facturation-end-mois.value":
        date_facturation: pd.DataFrame = get_facturation_date()

        year_date = date_facturation[
            date_facturation["Annee"] == inputs["date-facturation-end-annee"]["value"]
        ]

        outputs["date-facturation-end-jour"]["options"] = value_to_dropdown(
            year_date[year_date["Mois"] == trigger["value"]]["Jour"].values
        )

        return outputs

    if trigger["id"] == "date-facturation-end-jour.value":
        date_facturation: pd.DataFrame = get_facturation_date()

        year: str = str(inputs["date-facturation-end-annee"]["value"])
        month: str = str(inputs["date-facturation-end-mois"]["value"])
        day: str = str(trigger["value"])

        outputs["date-range-picker"]["end_date"] = "-".join([year, month, day])
        outputs = hide_date_warning(
            outputs,
            inputs,
            display=not is_facturation_date(inputs["date-range-picker"]["start_date"]),
        )
        return outputs

    print("TRIGGER non géré !")
    raise PreventUpdate


def disconnect(outputs: Dict[str, Dict[str, Any]], inputs: Dict[str, Dict[str, Any]]):
    """Documentation
    Deconnect l'utilisteurs, clear les variables de session ect..

    Parameter:
        outputs: Dictionnaire des sorties format callback
        inputs: Dictionnaire des entrées format callback

    Sortie:
        outputs: Les sorties mises a jours
    """
    if inputs["disconnect-btn"]["n_clicks"] == 0:
        raise PreventUpdate

    # TODO l'action de la deconnexion
    # Redirection
    outputs["url"]["pathname"] = "/login"
    logout_user()
    return outputs


def value_to_dropdown(values: list):
    """Documentation
    Mets en forme une liste de valeur pour correspondre a la structure des dropdown de dash

    Parameter:
        values: Liste de valeurs

    Sortie:
        liste de dictionnaire label/value

    """
    return [{"label": i, "value": i} for i in values if i is not None]


def valid_filter(outputs: Dict[str, Dict[str, Any]], inputs: Dict[str, Dict[str, Any]]):
    """Documentation
    Vérifie s'il manque des valeurs dans les filtres et affiche les informations

    Parameter:
        outputs: Dictionnaire des sorties format callback
        inputs: Dictionnaire des entrées format callback

    Sortie:
        outputs: Les sorties mises a jours
    """
    # S'il manque des valeurs obligatoire non selectionné, on ne fait rien
    if (
        inputs["date-range-picker"]["start_date"] is None
        or inputs["date-range-picker"]["end_date"] is None
        or inputs["select-id_cpt"]["value"] is None
    ):
        raise PreventUpdate

    start_date: datetime.datetime = datetime.datetime.strptime(
        inputs["date-range-picker"]["start_date"], "%Y-%m-%d"
    )
    end_date: datetime.datetime = datetime.datetime.strptime(
        inputs["date-range-picker"]["end_date"], "%Y-%m-%d"
    )

    # Tab 1:
    if inputs["tabs"]["value"] == "tab1":
        data: pd.DataFram = get_data(
            inputs["select-id_cpt"]["value"],
            start_date,
            end_date,
        )
        outputs["graph"]["figure"] = graph(
            inputs["select-id_cpt"]["value"], data, mode="markers"
        )

        # Tableau
        outputs["table"]["columns"], outputs["table"]["data"] = table(data)
        outputs["table"]["filter_action"] = "native"

    # Tab2:
    if inputs["tabs"]["value"] == "tab2":
        print(inputs["select-periode"]["value"])
        data: pd.DataFrame = get_conso(
            inputs["select-id_cpt"]["value"],
            start_date,
            end_date,
            inputs["select-periode"]["value"],
        )

        outputs["graph2"]["figure"] = graph(
            inputs["select-id_cpt"]["value"],
            data,
            x="TS",
            y="Conso",
            title="Consomation",
            xlabel=inputs["select-periode"]["value"],
            ylabel="Consomation",
        )
        outputs["table2"]["columns"], outputs["table2"]["data"] = table(data)
        outputs["table2"]["filter_action"] = "native"

    # Tab3:
    if inputs["tabs"]["value"] == "tab3":
        # TODO : TAB3, filtre seulement pour le SGE et choisir le client => affichage de ses informations
        # Encore a définir
        # Client: filtre bloqué sur le client concerné
        print("TAB 3 pas encore prete")
        raise PreventUpdate

    return outputs


def highlight_point(
    outputs: Dict[str, Dict[str, Any]],
    inputs: Dict[str, Dict[str, Any]],
    graph_name: str,
    table_name: str,
):
    """Documentation
    Mise en surbrillance les valeurs selectionnées sur le graphique dans le tableau.

    Parameter:
        outputs: Dictionnaire des sorties format callback
        inputs: Dictionnaire des entrées format callback
        graph_name: Nom du graphique
        table_name: Nom de la table où les valeurs seront mise en evidence

    Sortie:
        outputs: Les sorties mises a jours
    """
    style_cond = [{"if": {"column_id": "Index"}, "display": "None"}]
    style_cond = []
    # Filter pour afficher seulement les valeurs selectionné en premier
    filter_query = ""
    if inputs[graph_name]["selectedData"] is None:
        pass
    else:
        for point in inputs[graph_name]["selectedData"]["points"]:
            style_cond += [
                {
                    "if": {
                        # "column_id": "Index",
                        "filter_query": "{{Index}} = {}".format(point["customdata"][0]),
                    },
                    "backgroundColor": "rgb(255, 255, 0)",
                    "color": "black",
                }
            ]
            filter_query += "{Index}= " + str(point["customdata"][0]) + " or "
        filter_query = filter_query[:-4]

    outputs[table_name]["style_data_conditional"] = style_cond
    outputs[table_name]["filter_query"] = filter_query

    # TODO Choisir les colonnes interressante a afficher selon SGE et CLIENT
    # Colonne index utile pour la jointure entre le graph et le tableau

    return outputs


def change_tab(
    outputs: Dict[str, Dict[str, Any]], inputs: Dict[str, Dict[str, Any]], tab: str
):
    """Documentation
    Gestion du changement d'onglet

    Parameter:
        outputs: Dictionnaire des sorties format callback
        inputs: Dictionnaire des entrées format callback
        tab: Nom de l'onglet

    Sortie:
        outputs: Les sorties mises a jours
    """
    if tab == "tab1":
        outputs["select-periode"]["style"] = {"display": "None"}

    elif tab == "tab2":
        outputs["select-periode"]["style"] = {"display": "block"}

    elif tab == "tab3":
        pass

    return outputs


def hide_date_warning(
    outputs: Dict[str, Dict[str, Any]], inputs: Dict[str, Dict[str, Any]], display: bool
):
    """Documentation
    Affiche / cache le message d'avertissement des dates de facturation

    Parameter:
        outputs: Dictionnaire des sorties format callback
        inputs: Dictionnaire des entrées format callback
        display: True : L'affiche
                 False : Le cache

    Sortie:
        outputs: Les sorties mises a jours
    """
    if display:
        inputs["warning-date-facturation"]["style"].update({"display": "block"})
        outputs["warning-date-facturation"]["style"] = inputs[
            "warning-date-facturation"
        ]["style"]

    else:
        inputs["warning-date-facturation"]["style"].update({"display": "None"})
        outputs["warning-date-facturation"]["style"] = inputs[
            "warning-date-facturation"
        ]["style"]

    return outputs


# Callback côté client qui gere l'ouverture et la fermeture du menu des filtres
# namespace represente un groupe de fonction
# function_name : le nom de la fonction a executer
# Emplacement script.js
dash_app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="openNav"),
    Output("sideMenu", "hidden"),
    Input("sideMenu-btn", "n_clicks"),
)


if __name__ == "__main__":
    with app.app_context():
        # S'execute une fois le serveur lancé
        print("Serveur initialisé")

    # Run pour le debug / developpement
    # dash_app.enable_dev_tools(debug=True)
    # app.run(debug=True, port=8000)

    # Run une fois deployé
    from waitress import serve

    serve(app, host="0.0.0.0", port=8000)
