from enum import Enum
import os
import pygame

# Définis la taille de chaque entitée/tuile
CASE_SIZE = 64
OPTIONS_LINES_MARGIN = 62

# Nombre de mises à jour par seconde
TICKS_PER_SECONDS = 144

# Coefficient appliqué si le joueur bouge en diagonale
PLAYER_DIAGONAL_COEFF = 1

# Vitesse du joueur exprimée en pixels/s
DEFAULT_PLAYER_SPEED = 300.0
# Seuil à partir duquel nous appliquons la trigonométrie
# Également exprimée en pixels/s
SPEED_NORMALIZE_SEUIL = 300.0

# Cette variable permet de dessiner le nombre d'images par secondes et les coordonnées du joueur.
# Elle est utilisée à des fins de débogages lors de nos sessions de développements.
# Il n'est pas recommandé de les activer, des chutes du nombre d'images par secondes sont à prévoir !
DRAW_DEBUG_INFOS = True

# Ces variables servent à define des couleurs, points de vies, unites et données utiles au jeu en lui-même
# Veuillez ne pas modifier ces variables pour une expérience plus immersive ^^

# Vie par défaut du joueur
DEFAULT_PLAYER_LIFE = 20
# Défense par défaut du joueur
DEFAULT_PLAYER_DEFENSE = 50
# Vitesse d'animation du joueur (225ms)
PLAYER_ANIMATION_RATE = 0.225
# Couleur de l'effet de bouclier du joueur
PLAYER_SHIELD_COLOR = (83, 165, 216)
# Couleur de l'effet de vie du joueur
PLAYER_LIFE_COLOR = (227, 49, 49)
# Coordonnées du joueur lors d'une nouvelle partie
PLAYER_START_COORDS = (-4101, -6498)

# Vitesse du companion
# Non implémenté.
COMPANION_SPEED = 250.0
# Non implémenté.
COMPANION_DISTANCE_FROM_PLAYER = [-(CASE_SIZE * 1), CASE_SIZE * 1]
# Non implémenté.
DEFAULT_COMPANION_DISTANCE_FROM_PLAYER = [-(CASE_SIZE * 1), CASE_SIZE * 1]

# Emplacement des sauvegardes
SAVE_DIR = os.path.join(os.path.curdir, "saves")

# Interval des sauvegardes automatiques
# Exprimé en secondes
AUTO_SAVE_INTERVAL = 5*60  # 5*60s = 5m

# Définis le volume des sons joués
SOUND_CONFIG = {
    "play": True,
    "global": 100,  # 100%,
    "player": 100,  # 100%
    "music": 100,  # 100%
    "effects": 100,  # 100%
}


class MenuCategories(Enum):
    """
    Cet énumérateur permet de définir les différentes catégories possibles dans le menu
    """
    NO_ONE = 0
    OPTIONS = 1
    COMMANDS = 2
    SUCCESS = 3
    LOAD_GAME = 4
    CREDITS = 5


# Les touches liées à des actions
# Permet de personnaliser les touches
KEYS_BINDINGS = {
    "up": pygame.K_z,
    "down": pygame.K_s,
    "left": pygame.K_q,
    "right": pygame.K_d,
}


class GameStatus(Enum):
    """
    Cet énumérateur permet de déclarer les différents états possibles du jeu
    """
    MENU = 0
    GAME = 1
