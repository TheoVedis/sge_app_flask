from typing import List, Union
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


def get_id_cpt(client: Union[str, None] = None) -> List[str]:
    """Documentation
    Parametre:
        client: le nom du client, du compte connecté s'il doit être restreint
        # TODO enlever le None

    Sortie:
        la liste des id des compteurs
    """

    # A REMETTRE pour selectionner les ID_CPT
    # data: pd.DataFrame = pd.read_sql_query(
    #     "select distinct Id_CPT from Test.dbo.Histo"
    #     # "where Nom_client = '" + client + "'", # TODO A rajouter une fois la base client intégré
    #     " order by Id_CPT",
    #     conn,
    # )

    data: pd.DataFrame = pd.read_sql_query(
        "select distinct name from Test.dbo.extratanomalies order by name", conn
    )

    return list(data["name"])


def get_data(
    id_cpt: List[str], startDate: datetime.datetime, endDate: datetime.datetime
) -> pd.DataFrame:
    """Documentation
    A partir d'une paire de date, d'un id de capteur, cette fonction va interroger la base de donneée

    Parametre:
        id_cpt: une list d'id de compteur
        startDate: une date de départ
        endDate: une date d'arrive > startDate

    Sortie:
        data: DataFrame contenant les valeurs des compteurs et tout autres informations

    """

    # Requete sur la base classique
    # data: pd.DataFrame = pd.read_sql_query(
    #     "select * from"
    #     " Test.dbo.Histo"
    #     " where TS > '"
    #     + startDate.strftime("%d/%m/%Y")
    #     + "' and TS < '"
    #     + endDate.strftime("%d/%m/%Y")
    #     + "' and Id_CPT in ('"
    #     + "','".join(id_cpt)
    #     + "')"
    #     + " order by TS, Id_CPT",
    #     conn,
    # )

    # Requete sur la base avec les anomalies
    data: pd.DataFrame = pd.read_sql_query(
        "select Chrono, Name Id_CPT, Value, Quality, TS, Anomalie, Type_Anomalie from"
        " Test.dbo.extratanomalies"
        " where TS > '"
        + startDate.strftime("%d/%m/%Y")
        + "' and TS < '"
        + endDate.strftime("%d/%m/%Y")
        + "' and name in ('"
        + "','".join(id_cpt)
        + "')"
        + " order by TS, name",
        conn,
    )

    return data


def get_conso(
    id_cpt: List[str],
    startDate: datetime.datetime,
    endDate: datetime.datetime,
    periode: str,
) -> pd.DataFrame:
    """Documentation
    A partir d'une paire de date, d'une periode, d'un id de capteur cette fonction va calculer la consomation

    Parameter:
        id_cpt: list des id des compteurs
        start_date: une date départ
        end_date: une date d'arrive > start_date
        periode: Valeur prédéfini d'une periode sur laquel est calculé les consommation (ex: jours, trim, an, ...)

    Sortie:
        data: DataFrame contenant les consommations associées aux compteurs
    """

    if periode == "jour":
        data: pd.DataFrame = pd.read_sql_query(
            "select vc1.Id_CPT, datefromparts(YEAR(vc2.TS), MONTH(vc2.TS), DAY(vc2.TS)) TS, SUM(vc2.Value - vc1.Value) Conso"
            " from"
            " v_conso vc1,"
            " v_conso vc2"
            " where"
            " vc1.Id_CPT in " + "('" + "','".join(id_cpt) + "')"
            " and vc1.TS > '"
            + startDate.strftime("%d/%m/%Y")
            + "' and vc1.TS < '"
            + endDate.strftime("%d/%m/%Y")
            + "' and vc1.Id_CPT = vc2.Id_CPT"
            " and vc1.Num = vc2.Num - 1"
            " group by vc1.Id_CPT, datefromparts(YEAR(vc2.TS), MONTH(vc2.TS), DAY(vc2.TS))"
            " order by vc1.Id_CPT, datefromparts(YEAR(vc2.TS), MONTH(vc2.TS), DAY(vc2.TS))",
            con=conn,
        )

    # print(data)

    return data


if __name__ == "__main__":
    # print(get_id_cpt())
    date = datetime.datetime.strptime("01-09-2008", "%d-%m-%Y")
    date2 = datetime.datetime.strptime("01-10-2008", "%d-%m-%Y")

    id_cpt = ["EA0101", "EA0102"]

    # print(get_data(id_cpt, date, date2).TS)
    print(get_conso(id_cpt, date, date2, periode="jour"))
