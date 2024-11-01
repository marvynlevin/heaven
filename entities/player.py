import random
from math import floor

from entities.parent import Entity, EntityType, Movement
from constants import *
from typing import Tuple
from modules.inventory import *
from modules.camera import Camera
from modules.assets import *
from modules.sound import Sound, SoundsId, calc_sound_volume


class Player(Entity):
    """
    Cette class définis le joueur et est héritée de la class Entity
    """

    def __init__(
            self,
            coords: Tuple[int, int] = PLAYER_START_COORDS,
            layer: int = 0,
            name: str = "Player",
            defense: int = DEFAULT_PLAYER_DEFENSE,
            life: int = DEFAULT_PLAYER_LIFE
    ) -> None:
        super().__init__(coords, life, EntityType.PLAYER, "")

        self.layer = 0
        self.DEFAULT_LAYER = 0

        self.DEFAULT_LIFE = life
        self.DEFAULT_DEFENSE = defense

        self.layer = layer
        self.name = name
        self.defense = defense

        self.idling = True
        self.ticks = 0
        self.fps = -1

        # Système d'animation
        self.animation_frame = 0.0
        self.MAX_ANIMATION_FRAME = 3.0
        self.last_movement_tick = 0.0
        self.animation_ticks = 0.0

        # [EXPERIMENTAL]
        self.inventory = Inventory()
        self.current_item = WoodSword()
        self.inventory_open = False

        # On déclare l'attribut "foots" pour le nombre de pas
        self.foots = 0
        self.foots_sounds = [
            SoundsId.CRN_FTP_1, SoundsId.CRN_FTP_2, SoundsId.CRN_FTP_3, SoundsId.CRN_FTP_4,
            SoundsId.CRN_FTP_5, SoundsId.CRN_FTP_6, SoundsId.CRN_FTP_7
        ]

    def get_movement_animation(self) -> str:
        """
        Permet d'obtenir un identifiant d'image (animations)
        Prend en compte si le joueur est en mouvement ou non
        """
        if self.idling or self.inventory_open:
            if self.movement == Movement.LEFT:
                return "player_left"
            elif self.movement == Movement.RIGHT:
                return "player_right"
            elif self.movement in [Movement.UP, Movement.UP_LEFT, Movement.UP_RIGHT]:
                return "player_top"
            else:
                return "player_bottom"
        elif not self.inventory_open:
            if self.movement == Movement.LEFT:
                return f"player_left_{floor(self.animation_frame)}"
            elif self.movement == Movement.RIGHT:
                return f"player_right_{floor(self.animation_frame)}"
            elif self.movement in [Movement.UP, Movement.UP_LEFT, Movement.UP_RIGHT]:
                return f"player_top_{floor(self.animation_frame)}"
            else:
                return f"player_bottom_{floor(self.animation_frame)}"

    @staticmethod
    def is_health_bars_needed() -> bool:
        """
        Non implémenté.
        Requiert la fonctionnalité des dégâts et monstres.
        """
        return False

    @staticmethod
    def is_defense_bars_needed() -> bool:
        """
        Non implémenté.
        Requiert la fonctionnalité des dégâts et monstres.
        """
        return False

    def draw_remaining_defense(self, x: int, y: int, screen: pygame.Surface, mid_adder: int):
        """
        Non implémenté.
        Requiert la fonctionnalité des dégâts et monstres.
        """
        if not self.is_defense_bars_needed():
            return
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                x - 35 + mid_adder,
                y + 17 - 34 - mid_adder,
                70,
                9
            )
        )
        pygame.draw.rect(
            screen,
            PLAYER_SHIELD_COLOR,
            (
                x - 34 + mid_adder,
                y + 18 - 34 - mid_adder,
                floor(68 * (self.defense / self.DEFAULT_DEFENSE)),
                7
            )
        )

    def draw_remaining_life(self, x: int, y: int, screen: pygame.Surface, mid_adder: int):
        """
        Non implémenté.
        Requiert la fonctionnalité des dégâts et monstres.
        """
        if not self.is_health_bars_needed():
            return
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                x - 35 + mid_adder,
                y + 5 - 35 - mid_adder,
                70,
                9
            )
        )
        pygame.draw.rect(
            screen,
            PLAYER_LIFE_COLOR,
            (
                x - 34 + mid_adder,
                y + 6 - 35 - mid_adder,
                floor(68 * (self.life / self.DEFAULT_LIFE)),
                7
            )
        )

    def draw_current_item(self, screen: pygame.Surface, assets: Assets):
        """
        Non implémenté.
        Requiert la fonctionnalité de l'inventaire.
        """
        return

    def draw(self, screen: pygame.Surface, assets: Assets, camera: Camera, map):
        player_surface = assets.get(self.get_movement_animation())
        if not (player_surface is None):
            # On dessine le joueur au centre de l'écran
            # Indépendamment de la caméra
            x = (screen.get_width() // 2) - CASE_SIZE + (player_surface.get_width() // 2)
            y = (screen.get_height() // 2) - (CASE_SIZE // 2) - (player_surface.get_height() // 2)
            if player_surface.get_height() > CASE_SIZE:
                # Joueur plus grand.
                # Il faut le décaler sur la hauteur
                y += CASE_SIZE - (player_surface.get_height() // 4)
            screen.blit(player_surface, (x, y))

    def move(self, movement: Movement, vector: Tuple[int, int], camera: Camera, delta: float):
        """
        Permet le mouvement du joueur
        """
        # On sauvegarde le temps auquel a eu lieu le dernier mouvement
        if self.inventory_open or vector == (0, 0):
            return

        # On redéfinit la direction du mouvement s'il n'est pas identique
        self.last_movement_tick = self.ticks + delta

        if movement != self.movement:
            self.movement = movement

        # Si le joueur ne bougeait pas, on change ça
        if self.idling:
            self.idling = False

        # On ajoute les vecteurs au joueur et à la caméra
        # C'est toujours mieux que la caméra nous suive
        self.x += vector[0]
        camera.x += vector[0]

        self.y += vector[1]
        camera.y += vector[1]

    def update(self, frequence: pygame.time.Clock, delta: float, sounds: Sound):
        self.fps = frequence.get_fps()

        # On ajoute le delta au nombre de ticks du système d'animation 
        self.animation_ticks += delta

        # Si le joueur est en mouvement, on ajoute delta à l'attribut `ticks` pour les animations
        if not self.idling:
            self.ticks += delta

        # On vérifie que le nombre de ticks d'animation est supérieur ou égal au minimum de ticks pour demander une
        # animation
        # On définit une variable temporaire qui va permettre de savoir si on doit jouer un son
        play_foot_sound = False
        if self.animation_ticks >= PLAYER_ANIMATION_RATE:
            # On passe à l'animation suivante et on réinitialise les ticks d'animation
            self.animation_frame = (self.animation_frame + 1) % self.MAX_ANIMATION_FRAME
            self.animation_ticks = 0
            play_foot_sound = True

        # Si le joueur ne bouge plus, on le déclare en "IDLING" et on réinitialise les ticks
        if (self.ticks - self.last_movement_tick >= PLAYER_ANIMATION_RATE) and (not self.idling):
            self.idling = True
            self.ticks = 0
            self.animation_ticks = 0
            self.animation_frame = 0

        if play_foot_sound:
            # On incrémente de 2 le nombre de pas
            self.foots += 2

            # Avant de jouer un nouveau son de pas, on coupe les autres sons de pas
            for id in self.foots_sounds:
                sounds.stop_sound(id)

            # On joue un nouveau son de pas
            random_sound = self.foots_sounds[random.randint(0, len(self.foots_sounds) - 1)]
            sounds.play_sound(random_sound, loops=0, volume=calc_sound_volume(random_sound))
