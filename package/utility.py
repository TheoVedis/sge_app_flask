"""Documentation
Ce fichier va contenir toutes les fonctions utilitaires de ce projet.
"""

import random


def random_secret_key(length: int, size: int = 500) -> str:
    key = ""
    for i in range(length):
        key += chr(int(random.random() * size))

    return key


if __name__ == "__main__":
    print(random_secret_key(10))