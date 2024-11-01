from constants import CASE_SIZE
from typing import List
from math import *
import json

# On va charger les collisions du fichier en lecture unique et avec un encodage UTF-8
with open("./algo/collisions.json", 'r', encoding='utf-8') as f:
    # Ce tableau contiendra nos collisions de la carte
    START_COLLISIONS = json.load(f)  # json.load renvoi un objet python (dict, list, str, int...) à partir d'un string


def check_col(col: int) -> bool:
    """
    Fonction très simple
    vérifie si `col ` est 1, alias une collision pleine
    """
    return col == 1


def collisions_algo(collisions: List[List[int]], x: int, y: int) -> bool:
    """
    Prend en entrée un tableau 2D (symbolisant les collisions) et les coordonnées du joueur.
    Renvoi une boolean ; true s'il y a collision, false sinon.
    """

    # Si la tuile n'existe pas, on ne veut pas faire planter le programme
    # Alors, on bloque toute erreur
    try:
        # On récupère la tuile sur laquelle est le joueur
        # `x` et `y` sont des nombres flottants.
        # Nous les divisons par les dimensions d'une tuile afin d'obtenir le nombre de la tuile
        tile = collisions[abs(floor((y / CASE_SIZE)))][abs(floor(x / CASE_SIZE))]
        # On renvoie le résultat de la fonction `check_col`
        return check_col(tile)
    except:
        return False
