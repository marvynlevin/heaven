import datetime
from math import floor

import pygame.draw

from constants import *
from entities.player import Player
from constants import GameStatus
from modules.camera import Camera
from modules.fonts import fonts
from modules.save import saves, GameSave

"""
Ce fichier contient le menu pour charger une ancienne partie
"""


class LoadGame:
    """
    Cette class représente le menu pour charger une ancienne partie
    """

    def __init__(self) -> None:
        self.esc_to_close = fonts.get(20).render("[ECHAP] pour quitter ce menu", True, (240, 240, 240))
        self.no_save = fonts.get(35).render("Aucune partie sauvegardée.", True, (240, 240, 240))

        # On stocke la page actuelle
        self.actual_page = 0
        # On stocke le nombre maximal de pages
        self.MAX_PAGE = 0
        # On stocke la ligne à laquelle nous sommes
        self.actual_row = 0
        # On stocke le nombre maximal de lignes
        self.MAX_ROWS = 10

        # Cet attribut définis les délais entre deux lectures de touches
        # Pour que, si on reste appuyé sur la touche `UP`, nous puissions monter d'une ligne toutes les 0.2s (200 ms)
        self.key_cooldown = 0.2

        # On prépare le terrain pour afficher les sauvegardes
        self.saves = []

    def enter(self):
        """
        Cette fonction est appelée quand nous entrons dans ce menu
        """
        # On met à jour les sauvegardes depuis le disque dur
        saves.update()
        # on enregistre les nouvelles sauvegardes
        self.saves = saves.format(self.MAX_ROWS)

        # On met à jour le nombre maximal de pages et 
        # on réinitialise la page actuelle
        self.MAX_PAGE = len(self.saves)
        self.actual_page = 0

    def draw(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()

        # Fond
        pygame.draw.rect(
            screen,
            (0, 0, 0, 0),
            (
                100,
                100,
                screen_width - 200,
                screen_height - 200
            ),
            border_radius=25
        )
        pygame.draw.rect(
            screen,
            (20, 20, 20),
            (
                100,
                100,
                screen_width - 200,
                self.esc_to_close.get_height() + 40
            ),
            border_top_left_radius=25,
            border_top_right_radius=25
        )

        # Instruction pour revenir en arrière
        screen.blit(self.esc_to_close, (145, 120))

        # Message qu'aucune partie n'a été sauvegardée
        if len(self.saves) < 1 or (self.actual_page > len(self.saves) - 1) or len(self.saves[self.actual_page]) < 1:
            screen.blit(
                self.no_save,
                (
                    (screen_width // 2) - (self.no_save.get_width() // 2),
                    (screen_height // 2) - (self.no_save.get_height() // 2),
                )
            )
            return

        actual_saves = self.saves[self.actual_page]

        x, y = 190, 190

        # On va dessiner chaque sauvegarde de cette page
        for i in range(0, len(actual_saves)):
            # On appelle la bonne méthode
            self.draw_save(screen, actual_saves[i], x, y, self.actual_row == i)
            # On augmente `y` pour ne pas superposer les textes
            y += 64

        # On dessine maintenant les indicateurs de pages
        centered_page = self.MAX_PAGE // 2
        for p in range(0, self.MAX_PAGE):
            # On détermine la couleur
            if p == self.actual_page:
                color = (240, 240, 240)
            else:
                color = (90, 90, 90)
            # On vérifie s'il est à gauche
            if p < centered_page:
                pygame.draw.circle(
                    screen,
                    color,
                    center=(screen_width // 2 - ((centered_page - p) * 49), screen_height - 120),
                    radius=9
                )
            else:
                pygame.draw.circle(
                    screen,
                    color,
                    center=(screen_width // 2 + ((p - centered_page) * 49), screen_height - 120),
                    radius=9
                )

    @staticmethod
    def draw_save(screen: pygame.Surface, save: GameSave, x: int, y: int, selected: bool):
        """
        Cette fonction permet de dessiner une sauvegarde sur l'écran
        """
        height = 64

        # On dessine une magnifique ligne
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (200, y, screen.get_width() - 400, 1)
        )

        # Si la catégorie est sélectionnée, nous dessinons un point afin de montrer qu'elle est sélectionnée
        if selected:
            pygame.draw.circle(screen, (255, 255, 255), (x, y + (height // 2) + 3), radius=4)

        # On décale sur la droite
        x += 50

        save_name = fonts.get(25).render(f"Partie n'{save.id}", True, (255, 255, 255))
        screen.blit(save_name, (x, y + ((height // 2) - save_name.get_height() // 2)))

        # On génère le texte qui sera affiché pour la date

        # On calcule la durée écoulée en secondes depuis
        date_diff = (datetime.datetime.now() - save.date).total_seconds() / 60.0

        if date_diff < 60.0:
            # Il y a `n` minute
            date_text = f"Il y a {floor(date_diff)}m"
        elif 60.0 <= date_diff <= (24.0 * 60.0):
            # Il y a `n` heure
            date_text = f"Il y a {floor(date_diff / 60.0)}h"
        else:
            # Ça remonte à longtemps, on met la date complète
            date_text = save.date.strftime("%d/%m/%Y, %H:%M:%S")

        date = fonts.get(15).render(date_text, True, (255, 255, 255))
        screen.blit(date, (screen.get_width() - 200 - date.get_width(), y + 4))

        # On dessine une seconde ligne
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (200, y + height, screen.get_width() - 400, 1)
        )

    def reset_options_interface(self):
        """
        Cette fonction permet de réinitialiser cette catégorie quand nous la quittons
        """
        pass

    def enter_save(self, engine):
        """
        Cette fonction permet de charger une sauvegarde
        """

        # On récupère la sauvegarde
        if not ((self.actual_row + 1) in saves.saves):
            print("Unknown save: ", self.actual_row)
            return

        save: GameSave = saves.saves[self.actual_row + 1]

        # On prépare le tuple qui contient les coordonnées du joueur :)
        player_coordinates = (save.player_coords[0], save.player_coords[1])

        # On place le joueur et la caméra
        engine.game.camera = Camera(coords=player_coordinates)
        engine.game.player = Player(coords=player_coordinates)

        # On coupe les musiques
        engine.game.music.stop_sounds()

        # On coupe la cinématique
        engine.game.run_cinematic = False

        # On précise l'identifiant de sauvegarde en jeu
        engine.game.save_id = save.id

        # On ouvre le jeu et, surtout, nous fermons la catégorie
        engine.status = GameStatus.GAME
        engine.menu.ctg_open = MenuCategories.NO_ONE

    def update(self, delta: float):
        keys = pygame.key.get_pressed()

        # Si le cooldown de lecture des touches est inférieur ou nul, alors nous pouvons lire les touches
        if self.key_cooldown <= 0:
            # Nous redéfinissons le cooldown des touches
            self.key_cooldown = 0.2

            # Si la touche "Z" ou "UP" est pressée et que nous ne sommes pas dans le menu de modification des touches,
            # nous passons à la ligne supérieure
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.actual_row = ((self.actual_row - 1) % self.MAX_ROWS)
            # Si la touche "S" ou "DOWN" est pressée et que nous ne sommes pas dans le menu de modification des touches,
            # nous passons à la ligne inférieure
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.actual_row = ((self.actual_row + 1) % self.MAX_ROWS)

        elif self.key_cooldown > 0:
            # Sinon, nous ajoutons `delta` à l'attribut `key_cooldown` afin de réduire le temps avant la prochaine
            # lecture des touches
            self.key_cooldown -= delta

    def key_down(self, event, engine):
        # Une touche a été pressée, nous réinitialisons le cooldown
        self.key_cooldown = 0

        # Entrée dans une partie
        if (event.key == pygame.K_SPACE) or (event.key == pygame.K_RETURN):
            self.enter_save(engine)

        # Changement de pages
        if (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
            # changement de page vers la gauche si la touche "A" ou "LEFT" est pressée
            self.actual_page = (self.actual_page - 1) % self.MAX_PAGE
        elif (event.key == pygame.K_e) or (event.key == pygame.K_RIGHT):
            # changement de page vers la droite si la touche "E" ou "RIGHT" est pressée
            self.actual_page = (self.actual_page + 1 + self.MAX_PAGE) % self.MAX_PAGE


# Afin d'y accéder depuis plusieurs endroits, nous définissons une variable qui pourra être accédée
# de partout dans le code source
load: LoadGame = LoadGame()
