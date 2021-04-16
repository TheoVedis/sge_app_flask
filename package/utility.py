"""Documentation
Ce fichier va contenir toutes les fonctions utilitaires de ce projet.
"""

import datetime
import random
from typing import List
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from package.data_base_manager import get_data

import dash


def dash_kwarg(outputs, inputs, states):
    """Documentation
    S'applique apres un callback pour donner plusieur parametre a la fonction.
    Ordonne les parametres sous forme de dictionnaire.

    Parametre:
        outputs: les sorties d'un callback
        inputs: les entrées d'un callback
        states: les states d'un callback (entrées non declenchante)
    """

    def accept_func(func):
        def wrapper(*args):
            ctx: dash._callback_context.CallbackContext = dash.callback_context

            if len(ctx.triggered) > 1:
                print("context callback > 1 ? POSSIBLE ?!")

            if ctx:
                trigger = {
                    "id": ctx.triggered[0]["prop_id"],
                    "value": ctx.triggered[0]["value"],
                }
            else:
                trigger = (None, None)
                print("ERROR ?")

            out_dict = {}
            for item in outputs:
                try:
                    out_dict[item.component_id][
                        item.component_property
                    ] = dash.no_update
                except KeyError:
                    out_dict[item.component_id] = {
                        item.component_property: dash.no_update
                    }

            ind = 0
            input_dict = {}
            for item in inputs:
                try:
                    input_dict[item.component_id][item.component_property] = args[ind]
                except KeyError:
                    input_dict[item.component_id] = {item.component_property: args[ind]}
                ind += 1

            for item in states:
                try:
                    input_dict[item.component_id][item.component_property] = args[ind]
                except KeyError:
                    input_dict[item.component_id] = {item.component_property: args[ind]}
                ind += 1

            kwargs_dict = {
                "outputs": out_dict,
                "inputs": input_dict,
                "trigger": trigger,
            }
            return dash_return(func(**kwargs_dict))

        return wrapper

    return accept_func


def dash_return(outputs: dict):
    """Documentation
    Mise en forme des sorties pour correspondre aux attentes de Dash

    Parametre:
        outputs: Dictionnaires des sorties

    Sortie:
        listes des sorties et de leur valeur
    """
    out = []
    for component_id in outputs:
        for component_property in outputs[component_id]:
            out.append(outputs[component_id][component_property])

    return out


def random_secret_key(length: int, size: int = 500) -> str:
    """Documentation
    L'objectif de cette fonction est de générer une clef aléatoire pour le stockage des
    données de session.
    """
    key = ""
    for i in range(length):
        key += chr(int(random.random() * size))

    return key


def graph(id_cpt: List, start_date: str, end_date: str):
    """Documentation
    Crée les graphiques pour les afficher!
    TODO: sortir les get_data() et garder que la partie graph pour eviter plusieur appel
    """
    fig = go.Figure()

    for id in id_cpt:
        data = get_data(
            id,
            datetime.datetime.strptime(start_date, "%Y-%m-%d"),
            datetime.datetime.strptime(end_date, "%Y-%m-%d"),
        )
        fig.add_trace(
            go.Scatter(
                x=data["TS"],
                y=data["Value"],
                mode="markers",
                name=id,
            )
        )

    fig.update_layout(
        title="Valeurs des compteurs",
        xaxis_title="Date (heure)",
        yaxis_title="Valeur",
        legend_title="Id Compteur:",
        font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
    )

    return fig


if __name__ == "__main__":
    print(random_secret_key(10))

    date = datetime.datetime.strptime("01-10-2008", "%d-%m-%Y")
    date2 = datetime.datetime.strptime("02-10-2008", "%d-%m-%Y")

    id_cpt = "EA0101"

    # print(get_data(id_cpt, date, date2))
