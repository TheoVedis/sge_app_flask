"""Documentation
Ce fichier va contenir toutes les fonctions utilitaires de ce projet.
"""

import random
from typing import List
import plotly
import plotly.graph_objs as go
from package.data_base_manager import get_data
import pandas as pd
import json


def random_secret_key(length: int, size: int = 500) -> str:
    """Documentation
    L'objectif de cette fonction est de générer une clef aléatoire pour le stockage des
    données de session.
    """
    key = ""
    for i in range(length):
        key += chr(int(random.random() * size))

    return key


def graph(id_cpt: list, startDate, endDate):

    data: List[go.Scatter] = []
    for id in id_cpt:
        df: pd.DataFrame = get_data(id, startDate, endDate)
        data.append(go.Scatter(x=df["Chrono"], y=df["Value"]))

    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)


if __name__ == "__main__":
    print(random_secret_key(10))