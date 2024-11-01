from modules.assets import Assets
from modules.camera import *
from constants import *


class Movement(Enum):
    """
    Cet énumérateur permet de déclarer les différents mouvements possibles du joueur
    """
    UP = 0
    UP_RIGHT = 1
    UP_LEFT = 2
    LEFT = 3
    RIGHT = 4
    BOTTOM_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM = 7


class EntityType(Enum):
    """
    Cet énumarateur permet de déclarer les différentes entities
    """
    PLAYER = 0
    SPIRIT = 1
    COMPANION = 2


def determine_collision_move(movement: Movement, axe: 0 | 1) -> Movement | None:
    """
    Cette fonction permet de décomposer le mouvement selon l'axe.
    Les axes, déclarés par la variable `axe', peuvent être :
    - 0 : l'axe des abscisses (x)
    - 1 : l'axe des ordonnées (y)
    
    Si le `Movement` en entrée n'est que sur l'axe `x`, alors :
    - Si l'axe est 0 (x), on reçoit un Movement
    - Si l'axe est 1 (y), on reçoit None, car il n'y a de déplacement sur y
    
    Cette mécanique est réciproque et fonctionne également dans le cas où un mouvement est sur les axes X et Y
    simultanément.
    """
    if movement in [Movement.UP, Movement.BOTTOM]:
        if axe == 0:
            return None
        else:
            return movement
    elif movement in [Movement.RIGHT, Movement.LEFT]:
        if axe == 0:
            return movement
        else:
            return None
    elif movement == Movement.UP_RIGHT:
        if axe == 0:
            return Movement.RIGHT
        else:
            return Movement.UP
    elif movement == Movement.UP_LEFT:
        if axe == 0:
            return Movement.LEFT
        else:
            return Movement.UP
    elif movement == Movement.BOTTOM_LEFT:
        if axe == 0:
            return Movement.LEFT
        else:
            return Movement.BOTTOM
    elif movement == Movement.BOTTOM_RIGHT:
        if axe == 0:
            return Movement.RIGHT
        else:
            return Movement.BOTTOM


class Entity:
    """
    Cette class déclare les attributs et méthodes communes à chaque entitée
    """

    def __init__(self, coords: Tuple[int, int], life: int, entity_type: EntityType, asset: pygame.Surface) -> None:
        self.x = coords[0]
        self.y = coords[1]

        self.life = life
        self.type = entity_type
        self.asset = asset

        self.movement = Movement.BOTTOM

    def draw(self, screen: pygame.Surface, assets: Assets, camera: Camera):
        """
        Dessine l'entité selon le même fonctionnement que les textes dans `mod/collisions.py`
        """

        coords = (
            self.x + (screen.get_width() // 2) - (CASE_SIZE // 2) + camera.x,
            self.y + (screen.get_height() // 2) - (CASE_SIZE // 2) + camera.y
        )

        screen.blit(self.asset, coords)
