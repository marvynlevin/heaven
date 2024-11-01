from typing import Tuple
from constants import *


class Camera:
    """
    Cette class est primordiale pour le jeu
    La camera peut être assimilée à un décalage de toutes les images
    Les attributs `x` et `y` vont être additionnés aux coordonnées de chaque image/entitée (sauf interface utilisateur)
        pour décaler ces derniers.
    
    `x` et `y` s'expriment en pixels
    """

    def __init__(self, coords: Tuple[int, int] = PLAYER_START_COORDS, speed=DEFAULT_PLAYER_SPEED) -> None:
        self.x = coords[0]
        self.y = coords[1]
        # Cet attribut déclare la vitesse du joueur
        self.speed = speed
        # Nous gardons la vitesse de base quand on a besoin de la réinitialiser
        self.DEFAULT_SPEED = speed
