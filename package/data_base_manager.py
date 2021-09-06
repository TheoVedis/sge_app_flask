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

conn2: pyodbc.Connection = conn

# Test Local
config: Dict[str, Dict[str, str]] = {
    "table": {
        "client": {
            "nom_table": "Test.dbo.Liste_Clients",
            "id": "[ID_CLIENT]",
            "groupe": "[ID USER]",
            "acces": "[Accès WEB]",
            "mot_de_passe": "[PWD]",
        },
        "compteur": {
            "nom_table": "Test.dbo.Compteurs",
            "id_cpt": "[ID_CPT]",
            "id_client": "[ID_CLIENT]",
        },
        "batiment": {"nom_table": "Test.dbo.Batiments"},
        "compteur_batiment": {"nom_table": "Test.dbo.Compteurs_Batiments"},
        "histo": {"nom_table": "Test.dbo.Histo"},
        "base_temps": {"nom_table": "Test.dbo.Base_temps"},
    }
}

# TODO changer tout les requetes sous la forme:
"""
"select client.{} 
    from {} client
    where client.{} = {}".format(config[..], config[..], config[..])
"""

# SQL Server
config: Dict[str, Dict[str, str]] = {
    "table": {
        "client": {
            "nom_table": "Access_SGE.dbo.Liste_Clients",
            "ref": "REF_CLIENT",
            "id": "[N_CLIENT_FACTURE]",
            "groupe": "[ID USER]",
            "acces": "[Accès WEB]",
            "mot_de_passe": "[PWD]",
        },
        "compteur": {
            "nom_table": "Access_SGE.dbo.Compteurs",
            "id_cpt": "[ID_CPT]",
            "id_client": "[ID_CLIENT]",
            "nom_batiment": "BATIMENTS_COMPTES",
        },
        "batiment": {
            "nom_table": "Access_SGE.dbo.Batiments",
            "ref": "REF_BATIMENT",
            "ref_client": "REF_CLIENT",
            "nom": "NOM_BATIMENT",
        },
        "histo": {
            "nom_table": "BigData.dbo.Table_Index_Histo",
            "temps": "TS",
            "id_cpt": "ID_CPT",
            "anomalie": "ANOMALIE",
            "DJU": "DJU",
            "type_anomalie": "TYPE_ANOMALIE",
            "index_corrige": "INDEX_CORRIGE",
            "valeur": "VALUE",
        },
        "base_temps": {
            "nom_table": "BigData.dbo.Base_TempsSGE",
            "type": "DATE_DE_FACTURATION",
            "date": "DATE",
        },
    }
}


# TODO rajouter groupe a id_cpt / batiment
# TODO probleme selecteur type d'energie, tout les compteurs


def get_login_pwd() -> pd.DataFrame:
    """Documentation
    Accede a la BD et récupere les information nécessaire a la connexion

    Sortie:
        Renvoie le dataframe contenant l'id, le groupe et le mot de passe associer a chaque utilisateur
    """

    request = "select distinct"

    data: pd.DataFrame = pd.read_sql_query(
        "select distinct client.[ID USER] id, client.[PWD] pwd from "
        + config["table"]["client"]["nom_table"]
        + " client"
        + " where"
        + " client.[Accès WEB] = 1",
        conn2,
    )

    return data


def get_client_name_from_ref(ref: str) -> str:
    """Documentation
    A partir d'un ref client renvoie l'Intitule du client correspondant

    Parametre:
        ref: référence du client

    Sortie:
        L'intitule du client
    """
    data: pd.DataFrame = pd.read_sql_query(
        "select client.[NOM CLIENT FACTURE] NOM from "
        + config["table"]["client"]["nom_table"]
        + " client "
        + " where '"
        + ref
        + "' = client.[N° CLIENT FACTURE]",
        conn2,
    )

    if len(list(data["NOM"])) == 0:
        print(
            "ERROR client pas dans la table permettant les jointures (ref: " + ref + ")"
        )
        return None

    return str(list(data["NOM"])[0])


def get_id_cpt(
    client: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    name_bat: Union[str, None] = None,
    group: Union[str, None] = None,
) -> List[str]:
    """Documentation
    Parametre:
        client: l'intitule du client ([NOM CLIENT FACTURE]), du compte connecté s'il doit être restreint

    Sortie:
        la liste des id des compteurs
    """
    if client is None and type_energie is None and name_bat is None and group is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct Id_CPT from "
            + config["table"]["histo"]["nom_table"]
            + " order by Id_CPT",
            conn,
        )

        return list(data["Id_CPT"])

    # Si group non None
    if client is None and type_energie is None and name_bat is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct cpt.Id_CPT from "
            + config["table"]["client"]["nom_table"]
            + " client, "
            + config["table"]["compteur"]["nom_table"]
            + " cpt"
            + " where '"
            + group
            + "' = client.[ID USER]"
            + " and cpt.ID_CLIENT = client.[N° CLIENT FACTURE]",
            conn2,
        )
        return list(data["Id_CPT"])

    # Si client selectionné
    if type_energie is None and name_bat is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct cpt.Id_CPT from "
            + config["table"]["client"]["nom_table"]
            + " client, "
            + config["table"]["compteur"]["nom_table"]
            + " cpt"
            + " where '"
            + client
            + "' = client.[NOM CLIENT FACTURE]"
            + " and cpt.ID_CLIENT = client.[N° CLIENT FACTURE]",
            conn2,
        )
        return list(data["Id_CPT"])

    # Si type_energie selectionné et pas batiment
    if name_bat is None:
        if client is None:
            data: pd.DataFrame = pd.read_sql_query(
                "select distinct cpt.Id_CPT from "
                + config["table"]["compteur"]["nom_table"]
                + " cpt where '"
                + type_energie
                + "' = cpt.[TYPE ENERGIE]",
                conn2,
            )
        else:
            data: pd.DataFrame = pd.read_sql_query(
                "select distinct cpt.Id_CPT from "
                + config["table"]["compteur"]["nom_table"]
                + " cpt, "
                + config["table"]["client"]["nom_table"]
                + " client where '"
                + type_energie
                + "' = cpt.[TYPE ENERGIE] "
                + "and client.[NOM CLIENT FACTURE] = '"
                + client
                + "' and cpt.ID_CLIENT = client.[N° CLIENT FACTURE]",
                conn2,
            )
        return list(data["Id_CPT"])

    # Batiment selectionné
    if type_energie is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct cpt.Id_CPT from "
            + config["table"]["compteur"]["nom_table"]
            + " cpt, "
            + config["table"]["batiment"]["nom_table"]
            + " bat where '"
            + name_bat
            + "' = bat.Nom_Batiment"
            + " and cpt.[Réf Batiment] =  bat.[Réf Batiment]",
            conn2,
        )
    else:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct cpt.Id_CPT from "
            + config["table"]["compteur"]["nom_table"]
            + " cpt, "
            + config["table"]["batiment"]["nom_table"]
            + " bat where '"
            + name_bat
            + "' = bat.Nom_Batiment"
            + " and cpt.[Réf Batiment] = bat.[Réf Batiment]"
            + " and cpt.[TYPE ENERGIE] = '"
            + type_energie
            + "'",
            conn2,
        )

    return list(data["Id_CPT"])


def get_groupe():
    data: pd.DataFrame = pd.read_sql_query(
        "select distinct [ID USER] groupe from "
        + config["table"]["client"]["nom_table"],
        conn,
    )
    return list(data["groupe"])


def get_client(
    id_cpt: Union[str, None] = None,
    name_bat: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    group: Union[str, None] = None,
) -> List[str]:

    if group is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct client.[NOM CLIENT FACTURE] Nom_Client from "
            + config["table"]["client"]["nom_table"]
            + " client ",
            conn2,
        )
        return list(data["Nom_Client"])

    data: pd.DataFrame = pd.read_sql_query(
        "select distinct client.[NOM CLIENT FACTURE] Nom_Client from "
        + config["table"]["client"]["nom_table"]
        + " client"
        + " where client.[ID USER] = '"
        + group
        + "'",
        conn2,
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
        + config["table"]["compteur"]["nom_table"]
        + " cpt ",
        conn2,
    )
    return list(data["Type_Energie"])


def get_batiment(
    id_cpt: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    name_client: Union[str, None] = None,
    group: Union[str, None] = None,
) -> List[str]:
    # Cas Aucune préselection
    if name_client is None and group is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct Nom_Batiment from "
            + config["table"]["batiment"]["nom_table"],
            conn,
        )
        return list(data["Nom_Batiment"])

    if name_client is None:
        data: pd.DataFrame = pd.read_sql_query(
            "select distinct Nom_Batiment from "
            + config["table"]["batiment"]["nom_table"]
            + " bat, "
            + config["table"]["client"]["nom_table"]
            + " client where '"
            + group
            + "' = client.[ID USER]"
            + " and bat.Réfclient = client.Réfclient",
            conn2,
        )
        return list(data["Nom_Batiment"])

    # Cas client selectionné
    data: pd.DataFrame = pd.read_sql_query(
        "select distinct bat.Nom_Batiment from "
        + config["table"]["batiment"]["nom_table"]
        + " bat, "
        + config["table"]["client"]["nom_table"]
        + " client where '"
        + name_client
        + "' = client.[NOM CLIENT FACTURE]"
        + " and bat.Réfclient = client.Réfclient",
        conn2,
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
        "select * from "
        + config["table"]["histo"]["nom_table"]
        + " where TS >= '"
        + startDate.strftime("%d/%m/%Y")
        + "' and TS <= '"
        + endDate.strftime("%d/%m/%Y")
        + "' and Id_CPT in ('"
        + "','".join(id_cpt)
        + "')"
        + " order by TS, Id_CPT",
        conn,
    )

    return data


# Obselete
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
            "select Year(Date) Annee, Month(Date) Mois, Day(Date) Jour from "
            + config["table"]["base_temps"]["nom_table"]
            + " where date_de_facturation = 'date facturation' order by Date",
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
