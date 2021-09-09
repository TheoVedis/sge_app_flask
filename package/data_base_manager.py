from typing import Dict, List, Union
import pyodbc
import pandas as pd
import datetime
import json

from package.request_manager import Request, Condition
from pathlib import Path

CONFIG_PATH = str(Path(__file__).parent.parent) + r"\config.json"

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

# Param de connection
conn = pyodbc.connect(config["connexion"]["big_data"])
conn2 = pyodbc.connect(config["connexion"]["access"])


def get_login_pwd() -> pd.DataFrame:
    """Documentation
    Accede a la BD et récupere les information nécessaire a la connexion

    Sortie:
        Renvoie le dataframe contenant l'id, le groupe et le mot de passe associer a chaque utilisateur
    """

    request = (
        Request(distinct=True)
        .add_selector("client.{}".format(config["table"]["client"]["groupe"]), "id")
        .add_selector(
            "client.{}".format(config["table"]["client"]["mot_de_passe"]), "pwd"
        )
        .add_table(config["table"]["client"]["nom_table"], "client")
        .add_condition(
            Condition("client.{} = 1".format(config["table"]["client"]["acces"]), "AND")
        )
    )

    data: pd.DataFrame = request.run(conn2)

    return data


# DEPRECIATED
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
        request = (
            Request(distinct=True)
            .add_selector(
                "histo.{}".format(config["table"]["histo"]["id_cpt"]), "Id_CPT"
            )
            .add_table(config["table"]["histo"]["nom_table"], "histo")
            .set_order_by("Id_CPT")
        )

        data: pd.DataFrame = request.run(conn)

        return list(data["Id_CPT"])

    request = (
        Request(distinct=True)
        .add_selector("cpt.{}".format(config["table"]["compteur"]["id_cpt"]), "Id_CPT")
        .add_table(config["table"]["compteur"]["nom_table"], "cpt")
        .set_order_by("Id_CPT")
    )

    if client is not None or group is not None:
        # Lien entre la table cpt et client
        request.add_table(
            config["table"]["client"]["nom_table"], "client"
        ).add_condition(
            Condition(
                "cpt.{} = client.{}".format(
                    config["table"]["compteur"]["id_client"],
                    config["table"]["client"]["id"],
                ),
                "AND",
            ),
        )

    # Condition sur le groupe
    if group is not None:
        request.add_condition(
            Condition(
                "client.{} = '{}'".format(config["table"]["client"]["groupe"], group),
                "AND",
            )
        )

    # Condition sur le client
    if client is not None:
        request.add_condition(
            Condition(
                "client.{} = '{}'".format(config["table"]["client"]["nom"], client),
                "AND",
            )
        )

    # Condition sur le type d'énergie
    if type_energie is not None:
        request.add_condition(
            Condition(
                "cpt.{} = '{}'".format(
                    config["table"]["compteur"]["type_energie"], type_energie
                ),
                "AND",
            )
        )

    if name_bat is not None:
        # Jointure des tables batiment et compteur
        # request.add_table(config["table"]["batiment"]["nom_table"], "bat")
        # request.add_condition(
        #     Condition(
        #         "cpt.{} = bat.{}".format(
        #             config["table"]["compteur"]["nom_batiment"],
        #             config["table"]["batiment"]["nom"],
        #         ),
        #         "AND",
        #     )
        # )

        request.add_condition(
            Condition(
                "cpt.{} = '{}'".format(
                    config["table"]["compteur"]["nom_batiment"], name_bat
                )
            )
        )

    data: pd.DataFrame = request.run(conn2)

    return list(data["Id_CPT"])


def get_groupe() -> List[str]:
    """Documentation
    Récupère la liste des groupes
    """

    request: Request = (
        Request(distinct=True)
        .add_selector("client.{}".format(config["table"]["client"]["groupe"]), "groupe")
        .add_table(config["table"]["client"]["nom_table"], "client")
        .set_order_by("groupe")
    )

    data: pd.DataFrame = request.run(conn)

    return list(data["groupe"])


def get_client(
    id_cpt: Union[str, None] = None,
    name_bat: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    group: Union[str, None] = None,
) -> List[str]:
    """Documentation
    Récupère la liste des clients en fonction du groupe sélectionné
    """

    request: Request = (
        Request(distinct=True)
        .add_selector(
            "client.{}".format(config["table"]["client"]["nom"]), "Nom_Client"
        )
        .add_table(config["table"]["client"]["nom_table"], "client")
        .set_order_by("Nom_Client")
    )

    if group is not None:
        request.add_condition(
            Condition(
                "client.{} = '{}'".format(config["table"]["client"]["groupe"], group),
                "AND",
            )
        )

    data: pd.DataFrame = request.run(conn2)

    return list(data["Nom_Client"])


def get_type_energie(
    id_cpt: Union[str, None] = None,
    name_bat: Union[str, None] = None,
    name_client: Union[str, None] = None,
) -> List[str]:
    """Documentation
    On selectionne les types d'energie sans prendre en considération les autres filtres
    """
    request: Request = (
        Request(distinct=True)
        .add_selector(
            "cpt.{}".format(config["table"]["compteur"]["type_energie"]), "Type_Energie"
        )
        .add_table(config["table"]["compteur"]["nom_table"], "cpt")
        .set_order_by("Type_Energie")
    )

    data: pd.DataFrame = request.run(conn2)

    return list(data["Type_Energie"])


def get_batiment(
    id_cpt: Union[str, None] = None,
    type_energie: Union[str, None] = None,
    name_client: Union[str, None] = None,
    group: Union[str, None] = None,
) -> List[str]:
    """Documentation
    Récupère les noms de batiments en fonction du groupe et des clients sélectionnés
    """

    request: Request = (
        Request(distinct=True)
        .add_selector(
            "bat.{}".format(config["table"]["batiment"]["nom"]), "Nom_Batiment"
        )
        .add_table(config["table"]["batiment"]["nom_table"], "bat")
        .set_order_by("Nom_Batiment")
    )

    if group is not None or name_client is not None:
        # Ajout de la jointure entre les deux tables
        request.add_table(
            config["table"]["client"]["nom_table"], "client"
        ).add_condition(
            Condition(
                "bat.{} = client.{}".format(
                    config["table"]["batiment"]["ref_client"],
                    config["table"]["client"]["ref"],
                ),
                "AND",
            ),
        )

    if group is not None:
        request.add_condition(
            Condition(
                "client.{} = '{}'".format(config["table"]["client"]["groupe"], group)
            )
        )

    if name_client is not None:
        request.add_condition(
            Condition(
                "client.{} = '{}'".format(config["table"]["client"]["nom"], name_client)
            )
        )

    data: pd.DataFrame = request.run(conn2)

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

    request: Request = (
        Request()
        .add_selector("*")
        .add_table(config["table"]["histo"]["nom_table"])
        .add_condition(
            Condition(
                "{} >= '{}'".format(
                    config["table"]["histo"]["temps"], startDate.strftime("%d/%m/%Y")
                )
            )
        )
        .add_condition(
            Condition(
                "{} <= '{}'".format(
                    config["table"]["histo"]["temps"], endDate.strftime("%d/%m/%Y")
                )
            )
        )
        .add_condition(
            Condition(
                "{} in ('{}')".format(
                    config["table"]["histo"]["id_cpt"], "','".join(id_cpt)
                )
            )
        )
        .set_order_by(
            "{}, {}".format(
                config["table"]["histo"]["temps"], config["table"]["histo"]["id_cpt"]
            )
        )
    )

    data: pd.DataFrame = request.run(conn)

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


def get_facturation_date() -> pd.DataFrame:
    """Documentation
    Cette fonction renvoies les dates de facturation,
    elles sont récupéré de la BD une fois à chaque redémarage de l'application

    Sortie:
        FACTURATION_DATE: Liste des dates de facturation

    """
    global FACTURATION_DATE
    if FACTURATION_DATE is None:
        request: Request = (
            Request()
            .add_selector(
                "Year({})".format(config["table"]["base_temps"]["date"]), "Annee"
            )
            .add_selector(
                "Month({})".format(config["table"]["base_temps"]["date"]), "Mois"
            )
            .add_selector(
                "Day({})".format(config["table"]["base_temps"]["date"]), "Jour"
            )
            .add_table(config["table"]["base_temps"]["nom_table"])
            .add_condition(
                Condition(
                    "{} = '{}'".format(
                        config["table"]["base_temps"]["type"], "date facturation"
                    )
                )
            )
            .set_order_by(config["table"]["base_temps"]["date"])
        )

        data: pd.DataFrame = request.run(conn)
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
