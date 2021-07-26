from typing import Dict, List, Union
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

# Test Local
config: Dict[str, str] = {
    "table": {
        "client": "Test.dbo.Clients",
        "compteur": "Test.dbo.Compteurs",
        "batiment": "Test.dbo.Batiments",
        "compteur_batiment": "Test.dbo.Compteurs_Batiments",
        "histo": "Test.dbo.Histo",
        "base_temps": "Test.dbo.Base_temps",
    }
}


def get_id_cpt(
    client: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    name_bat: Union[str, None] = None,
) -> List[str]:
    """Documentation
    Parametre:
        client: l'intitule du client ([INTITULE CLIENT]), du compte connecté s'il doit être restreint
        # TODO enlever le None une fois la BD client

    Sortie:
        la liste des id des compteurs
    """

    if client is None and type_energie is None and name_bat is None:
        # A REMETTRE pour selectionner les ID_CPT
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct Id_CPT from "
            + config["table"]["histo"]
            + " order by Id_CPT",
            conn,
        )

        # data: pd.DataFrame = pd.read_sql_query(
        #     "select distinct name from Test.dbo.extratanomalies order by name", conn
        # )
        return list(data["Id_CPT"])

    # Si client selectionné
    if type_energie is None and name_bat is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct cpt.Id_CPT from "
            + config["table"]["client"]
            + " client, "
            + config["table"]["compteur"]
            + " cpt"
            + " where '"
            + client
            + "' = client.[INTITULE CLIENT]"
            + " and cpt.ID_CLIENT = client.ID_CLIENT",
            conn,
        )
        return list(data["Id_CPT"])

    # Si type_energie selectionné et pas batiment
    if name_bat is None:
        if client is None:
            data: pd.DataFrame = pd.read_sql_query(
                "select distinct cpt.Id_CPT from "
                + config["table"]["compteur"]
                + " cpt where '"
                + type_energie
                + "' = cpt.[TYPE ENERGIE]",
                conn,
            )
        else:
            data: pd.DataFrame = pd.read_sql_query(
                "select distinct cpt.Id_CPT from "
                + config["table"]["compteur"]
                + " cpt, "
                + config["table"]["client"]
                + " client where '"
                + type_energie
                + "' = cpt.[TYPE ENERGIE] "
                + "and client.[INTITULE CLIENT] = '"
                + client
                + "' and cpt.ID_CLIENT = client.ID_CLIENT",
                conn,
            )
        return list(data["Id_CPT"])

    # Batiment selectionné
    if type_energie is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct cpt.Id_CPT from "
            + config["table"]["compteur"]
            + " cpt, "
            + config["table"]["compteur_batiment"]
            + " cpt_bat, "
            + config["table"]["batiment"]
            + " bat where '"
            + name_bat
            + "' = bat.Nom_Batiment"
            + " and cpt.Réfcpt = cpt_bat.Réfcpt"
            + " and cpt_bat.RéfBatCPT = bat.[Réf Batiment]",
            conn,
        )
    else:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct cpt.Id_CPT from "
            + config["table"]["compteur"]
            + " cpt, "
            + config["table"]["compteur_batiment"]
            + " cpt_bat, "
            + config["table"]["batiment"]
            + " bat where '"
            + name_bat
            + "' = bat.Nom_Batiment"
            + " and cpt.Réfcpt = cpt_bat.Réfcpt"
            + " and cpt_bat.RéfBatCPT = bat.[Réf Batiment]"
            + " and cpt.[TYPE ENERGIE] = '"
            + type_energie
            + "'",
            conn,
        )

    return list(data["Id_CPT"])


def get_groupe():
    data: pd.DataFrame = pd.read_sql_query(
        "select distinct [GROUPE] groupe from " + config["table"]["client"], conn
    )
    return list(data["groupe"])


def get_client(
    id_cpt: Union[str, None] = None,
    name_bat: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    groupe: Union[str, None] = None,
) -> List[str]:

    if groupe is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct client.[INTITULE CLIENT] Nom_Client from "
            + config["table"]["client"]
            + " client ",
            conn,
        )
        return list(data["Nom_Client"])

    data: pd.DataFrame = pd.read_sql_query(
        "select distinct client.[INTITULE CLIENT] Nom_Client from "
        + config["table"]["client"]
        + " client"
        + " where client.[GROUPE] = '"
        + groupe
        + "'",
        conn,
    )
    return list(data["Nom_Client"])


def get_type_energie(
    id_cpt: Union[str, None] = None,
    name_bat: Union[str, None] = None,
    name_client: Union[str, None] = None,
) -> List[str]:
    """Documentation
    On selectionne les types d'energie sans prendre en considération les autres filtres
    """

    data: pd.DataFrame = pd.read_sql_query(
        "select distinct cpt.[TYPE ENERGIE] Type_Energie from "
        + config["table"]["compteur"]
        + " cpt ",
        conn,
    )
    return list(data["Type_Energie"])


def get_batiment(
    id_cpt: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    name_client: Union[str, None] = None,
) -> List[str]:
    # Cas Aucune préselection
    if name_client is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct Nom_Batiment from " + config["table"]["batiment"], conn
        )
        return list(data["Nom_Batiment"])

    # Cas client selectionné
    data: pd.DataFrame = pd.read_sql_query(
        "select distinct bat.Nom_Batiment from "
        + config["table"]["batiment"]
        + " bat, "
        + config["table"]["client"]
        + " client where '"
        + name_client
        + "' = client.[INTITULE CLIENT]"
        + " and bat.Réfclient = client.Réfclient",
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


FACTURATION_DATE: pd.DataFrame = None


def get_facturation_date():
    global FACTURATION_DATE
    if FACTURATION_DATE is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select Year(Date) Annee, Month(Date) Mois, Day(Date) Jour from Test.dbo.Base_temps where date_de_facturation = 'date facturation' order by Date",
            conn,
        )

        data = data.apply(pd.to_numeric)
        FACTURATION_DATE = data

    return FACTURATION_DATE


if __name__ == "__main__":
    # print(get_id_cpt())
    date = datetime.datetime.strptime("01-09-2008", "%d-%m-%Y")
    date2 = datetime.datetime.strptime("01-10-2008", "%d-%m-%Y")

    id_cpt = ["EA0101", "EA0102"]

    # print(get_data(id_cpt, date, date2).TS)
    # print(get_conso(id_cpt, date, date2, periode="jour"))

    print(get_client(name_bat="A1"))
