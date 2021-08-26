"""Documentation
Ce fichier va regrouper l'ensemble des fonctions de connexion
"""

from typing import Any, Dict, Type

import pandas as pd
from flask_login import UserMixin
from package.data_base_manager import get_login_pwd

account: pd.DataFrame = get_login_pwd()


class User(UserMixin):
    Users = {}

    def __init__(self, id, group, password) -> None:
        super().__init__()
        self.id = id
        self.username = id
        self.password = password
        self.name = group
        User.Users[id] = self

    def get_user(id):
        try:
            return User.Users[id]
        except:
            return None

    def is_admin(self) -> bool:
        return self.id == "SGE"


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
        return int(User.get_user(username).password != password)
    except AttributeError:
        pass

    return 2


for i, row in account.iterrows():
    User(row["id"], row["id"], row["pwd"])
