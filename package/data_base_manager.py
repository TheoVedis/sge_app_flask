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


def get_id_cpt(
    client: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    name_bat: Union[str, None] = None,
) -> List[str]:
    """Documentation
    Parametre:
        client: le nom du client, du compte connecté s'il doit être restreint
        # TODO enlever le None une fois la BD client

    Sortie:
        la liste des id des compteurs
    """

    if client is None and type_energie is None and name_bat is None:
        # A REMETTRE pour selectionner les ID_CPT
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct Id_CPT from Test.dbo.Histo"
            # "where Nom_client = '" + client + "'", # TODO A rajouter une fois la base client intégré
            " order by Id_CPT",
            conn,
        )

        # data: pd.DataFrame = pd.read_sql_query(
        #     "select distinct name from Test.dbo.extratanomalies order by name", conn
        # )
        return list(data["Id_CPT"])

    if type_energie is None and name_bat is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct vc.Id_CPT from v_webApp_client vc where '"
            + client
            + "' = vc.Nom_Client",
            conn,
        )
        return list(data["Id_CPT"])

    if name_bat is None:
        if client is None:
            data: pd.DataFrame = pd.read_sql_query(
                "select distinct vc.Id_CPT from v_webApp_client vc where '"
                + type_energie
                + "' = vc.Type_Energie",
                conn,
            )
        else:
            data: pd.DataFrame = pd.read_sql_query(
                "select distinct vc.Id_CPT from v_webApp_client vc where '"
                + type_energie
                + "' = vc.Type_Energie "
                + "and vc.Nom_Client = '"
                + client
                + "'",
                conn,
            )
        return list(data["Id_CPT"])

    if type_energie is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct vc.Id_CPT from v_webApp_client vc where '"
            + name_bat
            + "' = vc.Nom_Batiment",
            conn,
        )
    else:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct vc.Id_CPT from v_webApp_client vc where '"
            + type_energie
            + "' = vc.Type_Energie "
            + "and vc.Nom_Batiment = '"
            + name_bat
            + "'",
            conn,
        )

    return list(data["Id_CPT"])


def get_client(
    id_cpt: Union[str, None] = None,
    name_bat: Union[str, None] = None,
    type_energie: Union[str, None] = None,
) -> List[str]:

    # if id_cpt is None and name_bat is None and type_energie is None:
    data: pd.DataFrame = pd.read_sql_query(
        "select distinct Nom_Client from v_webApp_client", conn
    )
    return list(data["Nom_Client"])

    if id_cpt is None and type_energie is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct vc.Nom_Client from v_webApp_client vc where '"
            + name_bat
            + "' = vc.Nom_Batiment",
            conn,
        )
        return list(data["Nom_Client"])

    if id_cpt is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct Nom_Client from v_webApp_client vc where '"
            + type_energie
            + "' = vc.Type_Energie",
            conn,
        )
        return list(data["Nom_Client"])

    data: pd.DataFrame = pd.read_sql(
        "select distinct Nom_Client from v_webApp_client vc where '"
        + id_cpt
        + "' = vc.Id_CPT",
        conn,
    )

    return list(data["Nom_Client"])


def get_type_energie(
    id_cpt: Union[str, None] = None,
    name_bat: Union[str, None] = None,
    name_client: Union[str, None] = None,
) -> List[str]:
    # Cas Aucune préselection
    # if id_cpt is None and name_bat is None and name_client is None:

    data: pd.DataFrame = pd.read_sql_query(
        "select distinct Type_Energie from v_webApp_client", conn
    )
    return list(data["Type_Energie"])

    # Cas client selectionné
    if id_cpt is None and name_bat is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct vc.Type_Energie from v_webApp_client vc where '"
            + name_client
            + "' = vc.Nom_Client",
            conn,
        )
        return list(data["Type_Energie"])

    # Cas Batiment selectionné
    if id_cpt is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct Type_Energie from v_webApp_client vc where '"
            + name_bat
            + "' = vc.Nom_Batiment",
            conn,
        )
        return list(data["Type_Energie"])

    # Cas compteur selectionné
    data: pd.DataFrame = pd.read_sql(
        "select distinct Type_Energie from v_webApp_client vc where '"
        + id_cpt
        + "' = vc.Id_CPT",
        conn,
    )

    return list(data["Type_Energie"])


def get_batiment(
    id_cpt: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    name_client: Union[str, None] = None,
) -> List[str]:
    # Cas Aucune préselection
    if id_cpt is None and type_energie is None and name_client is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct Nom_Batiment from v_webApp_client", conn
        )
        return list(data["Nom_Batiment"])

    # Cas client selectionné
    if id_cpt is None and type_energie is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct vc.Nom_Batiment from v_webApp_client vc where '"
            + name_client
            + "' = vc.Nom_Client",
            conn,
        )
        return list(data["Nom_Batiment"])

    # Cas type_energie selectionné
    if id_cpt is None:
        if name_client is None:
            data: pd.DataFrame = pd.read_sql_query(
                "select distinct Nom_Batiment from v_webApp_client vc where '"
                + type_energie
                + "' = vc.Type_Energie",
                conn,
            )
        else:
            data: pd.DataFrame = pd.read_sql_query(
                "select distinct Nom_Batiment from v_webApp_client vc where '"
                + type_energie
                + "' = vc.Type_Energie"
                + " and vc.Nom_Client = '"
                + name_client
                + "'",
                conn,
            )

        return list(data["Nom_Batiment"])

    # Cas compteur selectionné
    data: pd.DataFrame = pd.read_sql(
        "select distinct Nom_Batiment from v_webApp_client vc where '"
        + id_cpt
        + "' = vc.Id_CPT",
        conn,
    )

    return list(data["Nom_Batiment"])


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

    if type(id_cpt) != list:
        id_cpt = [id_cpt]

    # Requete sur la base classique
    data: pd.DataFrame = pd.read_sql_query(
        "select * from"
        " Test.dbo.Histo"
        " where TS >= '"
        + startDate.strftime("%d/%m/%Y")
        + "' and TS <= '"
        + endDate.strftime("%d/%m/%Y")
        + "' and Id_CPT in ('"
        + "','".join(id_cpt)
        + "')"
        + " order by TS, Id_CPT",
        conn,
    )

    # Requete sur la base avec les anomalies
    # data: pd.DataFrame = pd.read_sql_query(
    #     "select Chrono, Name Id_CPT, Value, Quality, TS, Anomalie, Type_Anomalie from"
    #     " Test.dbo.extratanomalies"
    #     " where TS >= '"
    #     + startDate.strftime("%d/%m/%Y")
    #     + "' and TS <= '"
    #     + endDate.strftime("%d/%m/%Y")
    #     + "' and name in ('"
    #     + "','".join(id_cpt)
    #     + "')"
    #     + " order by TS, name",
    #     conn,
    # )

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
    # TODO Changer les requetes par de simple requetes sur des vues
    # Voir pour le calul de la conso

    # Requete conso par jour
    if periode == "jour":
        data: pd.DataFrame = pd.read_sql_query(
            "select vc1.Id_CPT, datefromparts(YEAR(vc2.TS), MONTH(vc2.TS), DAY(vc2.TS)) TS, SUM(vc2.Value - vc1.Value) Conso"
            " from"
            " v_conso vc1,"
            " v_conso vc2"
            " where"
            " vc1.Id_CPT in " + "('" + "','".join(id_cpt) + "')"
            " and vc1.TS >= '"
            + startDate.strftime("%d/%m/%Y")
            + "' and vc1.TS <= '"
            + endDate.strftime("%d/%m/%Y")
            + "' and vc1.Id_CPT = vc2.Id_CPT"
            " and vc1.Num = vc2.Num - 1"
            " group by vc1.Id_CPT, datefromparts(YEAR(vc2.TS), MONTH(vc2.TS), DAY(vc2.TS))"
            " order by vc1.Id_CPT, datefromparts(YEAR(vc2.TS), MONTH(vc2.TS), DAY(vc2.TS))",
            con=conn,
        )

    # Requete conso par mois
    if periode == "mois":
        data: pd.DataFrame = pd.read_sql_query(
            "select vc1.Id_CPT, datefromparts(YEAR(vc2.TS), MONTH(vc2.TS), 1) TS, SUM(vc2.Value - vc1.Value) Conso"
            " from"
            " v_conso vc1,"
            " v_conso vc2"
            " where"
            " vc1.Id_CPT in " + "('" + "','".join(id_cpt) + "')"
            " and vc1.TS >= '"
            + startDate.strftime("%d/%m/%Y")
            + "' and vc1.TS <= '"
            + endDate.strftime("%d/%m/%Y")
            + "' and vc1.Id_CPT = vc2.Id_CPT"
            " and vc1.Num = vc2.Num - 1"
            " group by vc1.Id_CPT, datefromparts(YEAR(vc2.TS), MONTH(vc2.TS), 1)"
            " order by vc1.Id_CPT, datefromparts(YEAR(vc2.TS), MONTH(vc2.TS), 1)",
            con=conn,
        )

    # Requete pour la consomation par trimestre
    if periode == "trim":
        data: pd.DataFrame = pd.read_sql_query(
            "select vc1.Id_CPT, YEAR(vc2.TS) + MONTH(vc2.TS) / 3 / 10. TS, SUM(vc2.Value - vc1.Value) Conso"
            " from"
            " v_conso vc1,"
            " v_conso vc2"
            " where"
            " vc1.Id_CPT in " + "('" + "','".join(id_cpt) + "')"
            " and vc1.TS >= '"
            + startDate.strftime("%d/%m/%Y")
            + "' and vc1.TS <= '"
            + endDate.strftime("%d/%m/%Y")
            + "' and vc1.Id_CPT = vc2.Id_CPT"
            " and vc1.Num = vc2.Num - 1"
            " group by vc1.Id_CPT, YEAR(vc2.TS) + MONTH(vc2.TS) / 3 / 10."
            " order by vc1.Id_CPT, YEAR(vc2.TS) + MONTH(vc2.TS) / 3 / 10.",
            con=conn,
        )

    if periode == "sge":
        pass

    # print(data)

    return data


if __name__ == "__main__":
    # print(get_id_cpt())
    date = datetime.datetime.strptime("01-09-2008", "%d-%m-%Y")
    date2 = datetime.datetime.strptime("01-10-2008", "%d-%m-%Y")

    id_cpt = ["EA0101", "EA0102"]

    # print(get_data(id_cpt, date, date2).TS)
    # print(get_conso(id_cpt, date, date2, periode="jour"))

    print(get_client(name_bat="A1"))
