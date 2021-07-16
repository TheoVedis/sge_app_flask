"""Documentation
Ce fichier va regrouper l'ensemble des fonctions de connexion
"""

# TODO garder en memoire les connexion et les deconnecter au bout d'un certrain temps

from typing import Any, Dict, Type


account = {"test": "mdp", "test2": "mdp"}

from flask_login import UserMixin


class User(UserMixin):
    Users = {}

    def __init__(self, id, username, password) -> None:
        super().__init__()
        self.id = id
        self.username = username
        self.password = password
        User.Users[id] = self

    def get_user(id):
        try:
            return User.Users[id]
        except:
            return None


def is_logged(current_user: User) -> bool:
    """Documentation
    Verifie si un utilisateur est connecté.

    Parametre:
        data: dictionnaire des données session de l'utilisateur

    Sortie:
        True: L'utilisateur est connecté
        False: l'utilistauer n'est pas connecté
    """

    return current_user.is_authenticated


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


for username, password in account.items():
    User(username, username, password)