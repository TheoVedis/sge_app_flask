"""Documentation
Ce fichier va regrouper l'ensemble des fonctions de connexion
"""

from flask import Markup

account = {"test": "mdp"}


def is_logged(data: dict) -> bool:
    """Documentation
    Verifie si un utilisateur est connecté.

    Parametre:
        data: dictionnaire des données session de l'utilisateur

    Sortie:
        True: L'utilisateur est connecté
        False: l'utilistauer n'est pas connecté
    """

    if "is_logged" not in data:
        return False

    return data["is_logged"]


def msg_feedback(succes: int) -> str:
    """Documentation
    Genre le message d'erreur en cas de connexion

    Parametre:
        succes: indique le type d'erreur

    Sortie:
        Le message d'erreur
    """

    if succes == 1:
        return "Mot de passe incorrect"
    elif succes == 2:
        return "Nom de compte incorrect"

    return "Connexion reussi !"


def check_password(username: str, password: str) -> int:
    """Documentation
    Verifie le couple (username, password) et renvoie une valeur en fonction

    Parametre:
        username: Nom d'utilisateur
        password: Mot de passe

    Sortie:
        0: Connexion reussie
        1: Mot de passe incorrect
        2: Nom d'utilisateur inconnue
    """
    try:
        return int(account[username] != password)
    except KeyError:
        pass

    return 2
