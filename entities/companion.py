from math import *
from entities.parent import Entity, EntityType, Movement
from entities.player import Player
from modules.assets import Assets
from modules.camera import Camera
from constants import *
from typing import Tuple
from entities.parent import determine_collision_move

"""

[!] Code bugué

Il est requis de concevoir un algorithme de recherche de chemin (path finding), ce qui est assez gourmand, en temps et en ressources

Par conséquent, dû à la difficulté, il sera implémenté si nous avons du temps supplémentaire.

"""


def determine_move(vec: Tuple[int, int]) -> Movement:
    """
    Permet de déterminer les mouvements à partir d'un vecteur
    """
    if vec[0] > 0 and vec[1] == 0:
        return Movement.RIGHT
    elif vec[0] < 0 and vec[1] == 0:
        return Movement.LEFT
    elif vec[0] == 0 and vec[1] > 0:
        return Movement.UP
    elif vec[0] == 0 and vec[1] < 0:
        return Movement.BOTTOM
    elif vec[0] < 0 and vec[1] < 0:
        return Movement.BOTTOM_LEFT
    elif vec[0] > 0 > vec[1]:
        return Movement.BOTTOM_RIGHT
    elif vec[0] < 0 < vec[1]:
        return Movement.UP_LEFT
    elif vec[0] > 0 > vec[1]:
        return Movement.UP_RIGHT
    else:
        return Movement.BOTTOM


class Companion(Entity):
    """
    Cette class déclare un companion hérité de la class Entity
    """

    def __init__(self, x=0, y=0) -> None:
        super().__init__((x, y), 5, EntityType.COMPANION, "companion_idle_0")

        self.animation_frame = None
        self.last_movement_tick = None
        self.movement = Movement.BOTTOM
        self.idling = True
        self.ticks = 0

    def update(self, frequence: pygame.time.Clock, player: Player, camera: Camera, map, delta: float):
        # On est le joueur
        self.follow_player(frequence, player, camera, map, delta)

    def get_movement_animation(self) -> str:
        """
        Permet d'obtenir un identifiant d'image (animations)
        Prend en compte si le joueur est en mouvement ou non
        """
        if self.idling:
            if self.movement == Movement.LEFT:
                return "companion_left_idle"
            elif self.movement == Movement.RIGHT:
                return "companion_right_idle"
            elif self.movement in [Movement.UP, Movement.UP_LEFT, Movement.UP_RIGHT]:
                return "companion_up_idle"
            else:
                return "companion_down_idle"
        else:
            if self.movement == Movement.LEFT:
                return f"companion_left_{floor(self.animation_frame)}"
            elif self.movement == Movement.RIGHT:
                return f"companion_right_{floor(self.animation_frame)}"
            elif self.movement in [Movement.UP, Movement.UP_LEFT, Movement.UP_RIGHT]:
                return f"companion_up_{floor(self.animation_frame)}"
            else:
                return f"companion_down_{floor(self.animation_frame)}"

    def move(self, movement: Movement, vector: Tuple[int, int], delta: float):
        """
        Permet le mouvement du companion
        """
        # On sauvegarde le temps auquel a eu lieu le dernier mouvement
        self.last_movement_tick = self.ticks * delta

        # On redéfinit la direction du mouvement s'il n'est pas identique
        if movement != self.movement:
            self.movement = movement

        # Si le companion ne bougeait pas, on change ça
        if self.idling:
            self.idling = False

        # On ajoute les vecteurs
        self.x -= vector[0]
        self.y -= vector[1]

    def manage_collisions(self, vec: Tuple[float, float], movement: Movement, map) -> Tuple[int, int]:

        """
        
        /!\ Code obsolète
        
        Le système de collisions a été totalement revu.
        
        """

        for collision in map.actual_zone.collisions:
            top_x = collision[0] + CASE_SIZE
            top_y = collision[1] + CASE_SIZE
            bottom_x = -(-top_x + collision[2])
            bottom_y = -(-top_y + collision[3])

            x = self.x + vec[0]
            y = self.y + vec[1]

            if (top_x >= x) and (top_y >= y) and (bottom_x <= x + CASE_SIZE) and (bottom_y <= y + CASE_SIZE):
                if movement in [Movement.UP, Movement.UP_LEFT, Movement.UP_RIGHT, Movement.BOTTOM, Movement.BOTTOM_LEFT,
                                Movement.BOTTOM_RIGHT]:
                    vec = (vec[0], 0)
                if movement in [Movement.RIGHT, Movement.UP_RIGHT, Movement.UP_LEFT, Movement.LEFT,
                                Movement.BOTTOM_LEFT, Movement.BOTTOM_RIGHT]:
                    vec = (0, vec[1])

                # Check x & y
                x_check = determine_collision_move(movement, 0)
                if x_check == movement:
                    return 0, 0
                elif not (x_check is None):
                    vec = (0, vec[1])
                y_check = determine_collision_move(movement, 1)
                if y_check == movement:
                    return 0, 0
                elif not (y_check is None):
                    vec = (vec[0], 0)

        return vec

    def follow_player(self, frequence: pygame.time.Clock, player: Player, camera: Camera, map, delta: float):

        """
        
        /!\ Code obsolète
        
        Le système de déplacement/de collisions a été amélioré et les changements n'ont pas été portés ici dû à
        la complexité requise (path finding)
        
        """

        distance_interval = COMPANION_DISTANCE_FROM_PLAYER

        px, py = (player.x, player.y)

        distance_x = px - self.x
        distance_y = py - self.y

        # On vérifie si le compagnon est à distance correcte (COMPANION_DISTANCE_FROM_PLAYER)
        if (distance_interval[0] <= distance_x <= distance_interval[1]) and (
                distance_interval[0] <= distance_y <= distance_interval[1]):
            return

        # Ok donc on doit le bouger
        # Laissez nous sortir le compas et la règle

        vec: Tuple[int, int] = (0, 0)

        if distance_x > COMPANION_SPEED:
            vec = (-COMPANION_SPEED, 0)
        elif distance_x < COMPANION_SPEED:
            vec = (COMPANION_SPEED, 0)
        else:
            vec = (distance_x, 0)

        if distance_y > COMPANION_SPEED:
            vec = (vec[0], -COMPANION_SPEED)
        elif distance_y < COMPANION_SPEED:
            vec = (vec[0], COMPANION_SPEED)
        else:
            vec = (vec[0], distance_y)

        # Normaliser vecteurs
        total_speed = sqrt(vec[0] ** 2 + vec[1] ** 2)
        if total_speed > SPEED_NORMALIZE_SEUIL:
            normalization_coeff = SPEED_NORMALIZE_SEUIL / total_speed
            vec = (vec[0] * normalization_coeff, vec[1] * normalization_coeff)

        # self.move(determine_move(vec), vec, camera, frequence.get_fps())

        movement = determine_move(vec)

        print(movement, vec)

        vec = self.manage_collisions((vec[0] * delta, vec[1] * delta), movement, map)

        # Move companion based on his movement
        decompose_x = determine_collision_move(movement, 1)
        if not (decompose_x is None):
            if vec[0] != 0:
                self.move(movement, (vec[0], 0), frequence.get_fps())

        decompose_y = determine_collision_move(movement, 0)
        if not (decompose_y is None):
            if vec[1] != 0:
                self.move(movement, (0, vec[1]), frequence.get_fps())

    def draw(self, screen: pygame.Surface, assets: Assets, camera: Camera, map):
        player_surface = assets.get(self.asset)
        if not (player_surface is None):
            x = (-self.x) + camera.x + (map.zone_decals[0] // 2)
            y = (-self.y) + camera.y + (map.zone_decals[1] // 2)
            screen.blit(player_surface, (x, y))


"""



        if distance_x >= COMPANION_SPEED:
            vec = (COMPANION_SPEED, 0)
        elif distance_x <= -COMPANION_SPEED:
            vec = (-COMPANION_SPEED, 0)
        else:
            vec = (-COMPANION_SPEED, 0)

        if distance_y >= COMPANION_SPEED:
            vec = (vec[0], COMPANION_SPEED)
        elif distance_y <= -COMPANION_SPEED:
            vec = (vec[0], -COMPANION_SPEED)
        else:
            vec = (vec[0], distance_y)

        # # On détermine dans quel sens il doit aller
        # if (px - self.x) < (px - self.x) + vec[0]:
        #     # Il doit aller sur la droite, on inverse X
        #     vec = (-vec[0], vec[1])
        # if (px - self.y) < (py - self.y) + vec[1]:
        #     # Il doit aller sur la droite, on inverse Y
        #     vec = (vec[0], -vec[1])

"""
