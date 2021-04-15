from typing import List
import pyodbc
import pandas as pd
import datetime

# Param de connection
conn: pyodbc.Connection = pyodbc.connect(
    "driver={SQL Server};"
    "server=SGE-PC-107;"
    "DATABASE=Test;"
    "Trusted_Connection=yes;"
)


def get_id_cpt(client: str = None) -> List[str]:
    """Documentation
    Parametre:
        client: le nom du client, du compte connecté s'il doit être restreint

    Sortie:
        la liste des id des compteurs
    """

    data: pd.DataFrame = pd.read_sql_query(
        "select distinct Id_CPT from Test.dbo.Histo"
        # "where Nom_client = '" + client + "'", # A rajouter une fois la base client intégré
        " order by Id_CPT",
        conn,
    )

    return list(data["Id_CPT"])


def get_data(
    id_cpt, startDate: datetime.datetime, endDate: datetime.datetime
) -> pd.DataFrame:
    """Documentation
    Parametre:
        id_cpt: un id de capteur
        startDate: une date de départ
        endDate: une date d'arrive < startDate

    Sortie:
        data: DataFrame contenant les valeurs des compteurs et tout autres informations

    """

    data: pd.DataFrame = pd.read_sql_query(
        "select * from"
        " Test.dbo.Histo"
        " where TS > '"
        + startDate.strftime("%d/%m/%Y")
        + "' and TS < '"
        + endDate.strftime("%d/%m/%Y")
        + "' and Id_CPT = '"
        + str(id_cpt)
        + "'",
        conn,
    )

    return data


if __name__ == "__main__":
    print(get_id_cpt())
