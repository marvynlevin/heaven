from enum import Enum
from math import floor
import pygame
from typing import List, Tuple
from modules.fonts import fonts

"""

    --- EXPLICATIONS ---
        
Pour le système de cinématique, nous avons choisi cette stratégie:
- Chaque image de fond est déclarée par la class `CinematicAsset`
- Chaque texte est déclaré par la class `CinematicText`
- Les fonds sont toujours dessinés en dessous des textes (alias. dessinés avant les textes)

Chaque texte et image possède un interval de temps basé sur le delta.
Pour rappel, le delta est un nombre flottant exprimant le temps exacte écoulé.

A chaque début de cinématique, le delta commence à 0
"""


class CinematicAsset:
    """
    Cette class permet de déclarer une image de fond
    """

    def __init__(
            self,
            name: str,
            asset: pygame.Surface,  # l'image en elle-même
            start: float,  # delta correspondant au début de la durée d'apparition du fond
            end: float,  # delta correspondant à la fin de la durée d'apparition du fond
            center: bool,  # Déclare si l'image doit être centrée
            coords: Tuple[float, float] = (0, 0),  # Déclare les coordonnées de l'image SUR L'ÉCRAN
            continue_drawing: bool = True  # Declare si il y a un mouvement d'animation verticale
    ) -> None:
        self.name = name
        self.asset = asset
        self.start = start
        self.end = end

        self.center = center
        self.coords = coords
        self.continue_drawing = continue_drawing

    def is_middled(self, ticks: float):
        """
        Renvoi une boolean pour savoir si les ticks sont entre les propriétés start et end
        """
        return self.start <= ticks <= self.end

    def draw(self, screen: pygame.Surface, delta: float) -> None:
        # On vérifie si l'image doit être centrée
        if not self.center:
            # Si c'est non, on dessine l'image aux coordonnées en claire
            screen.blit(self.asset, self.coords)
            # Si l'animation verticale est activée :
            if self.continue_drawing:
                # Delta correspond au décalage sur y
                while delta < self.asset.get_height():
                    # On dessine l'image une seconde fois en appliquant le delta
                    screen.blit(
                        self.asset,
                        (
                            self.coords[0],
                            self.coords[1] - delta,
                        )
                    )
                    # On incrémente le delta de la hauteur de l'image
                    #   afin d'être sûr que si une autre image doit être dessinée
                    #   alors, elles ne se chevaucheront pas
                    delta += self.asset.get_height()
        else:
            # On récupère les dimensions de l'écran
            sw, sh = screen.get_size()
            # On dessine l'image Pour x et y, on calcule de cette façon : Moitié de l'axe (n//2), et on retire la
            # moitié de la dimension sur cet axe pour que le centre de l'image soit au centre. Ce qui fait: x: (
            # screen_width // 2) - (image_width // 2) y: (screen_height // 2) - (image_height // 2)
            screen.blit(
                self.asset,
                (
                    (sw // 2) - (self.asset.get_width() // 2),
                    (sh // 2) - (self.asset.get_height() // 2) - delta
                )
            )
            # Si l'animation verticale est activée :
            if self.continue_drawing:
                # Delta correspond au décalage sur y
                while delta < self.asset.get_height():
                    # On dessine l'image une seconde fois en appliquant le delta.
                    # Nous utilisons les mêmes règles des coordonnées
                    screen.blit(
                        self.asset,
                        (
                            (sw // 2) - (self.asset.get_width() // 2),  # self.coords[0],
                            (sh // 2) - (self.asset.get_height() // 2) - delta  # self.coords[1] - delta,
                        )
                    )
                    # On incrémente le delta de la hauteur de l'image
                    #   afin d'être sûr que si une autre image doit être dessinée
                    #   alors, elles ne se chevaucheront pas
                    delta += self.asset.get_height()


class Position(Enum):
    """
    Précise la position du texte dans l'écran
    L'utilisation d'une class d'énumération permet de ne pas
        avoir de soucis si la fenêtre est redimensionnée
    """
    BOTTOM = 0
    MIDDLE = 1
    UP = 2


class CinematicText:
    """
    Cette class permet de déclarer un texte
    Le fonctionnement est identique à `CinematicAsset', excepté que c'est un texte
    """

    def __init__(
            self,
            name: str,
            asset: pygame.Surface,
            start: float,
            end: float,
            center: bool = True,
            position: Position = Position.MIDDLE,
            coords: Tuple[float, float] = (0, 0)
    ) -> None:
        """
        Propriétés passées en arguments :
        identiques à CinematicAsset, sauf:
        - position: Précise la position du texte

        /!\ ATTENTION: les valeurs "start" et "end" doivent inclures le temps de l'animation !!!
        """
        self.animation_duration = None
        self.name = name
        self.asset = asset
        self.ALPHA = self.asset.get_alpha()
        self.start = start
        self.end = end

        self.center = center
        self.coords = coords

        self.position = position

    def is_middled(self, ticks: float):
        """
        Renvoi une boolean pour savoir si les ticks sont entre les propriétés start et end
        """
        return self.start <= ticks <= self.end

    def detect_animation(self, ticks: float) -> 0 | 1 | 2:
        """
        Renvoi le statut de l'animation
        0 = animation de début
        1 = pas d'animation
        2 = animation de fin
        """
        if self.start + self.animation_duration >= ticks:
            return 0
        elif self.end - self.animation_duration >= ticks:
            return 2
        else:
            return 1

    def draw(self, screen: pygame.Surface) -> None:
        if not self.center:
            screen.blit(self.asset, self.coords)
        else:
            # On récupère la taille de l'écran
            sw, sh = screen.get_size()

            # Idem que `CinematicAsset`
            x, y = (
                (sw // 2) - (self.asset.get_width() // 2) + self.coords[0],
                (sh // 2) - (self.asset.get_height() // 2) + self.coords[1]
            )

            # On modifie y selon la position déclarée du texte (self.position), voir l'énumarateur `Position`
            if self.position == Position.BOTTOM:
                y += sh // 4
            elif self.position == Position.UP:
                y -= sh // 4

            # On dessine le text
            screen.blit(self.asset, (x, y))


class CinematicID(Enum):
    """
    Cet énumérateur permet de déclarer quelle cinématique est en cours
    Beaucoup plus efficace/robuste qu'un nombre/string
    """
    BEGINNING = 0


class Cinematic:
    """
    Moteur permettant de gérer les cinématiques
    """

    def __init__(
            self,
            assets: List[CinematicAsset],  # Une liste d'images de fonds, possiblement vide
            # Tuple[str, float, float, pygame.Surface, Tuple[float, float]]
            texts: List[CinematicText],  # Une liste de textes, possiblement vide
            max_timeline: float,  # Le delta à lequel la cinématique s'arrêtera, s'exprime en secondes
            fill: bool = False,  # Si on remplit le fond
            fill_color: Tuple[int, int, int] = (0, 0, 0)  # Dépend de l'attribut `fill', déclare la couleur de fond
    ) -> None:
        self.assets = assets

        self.texts = texts
        self.max_timeline = max_timeline

        self.ticks = 0

        self.pause = False

        self.started = False

        self.fill = fill
        self.fill_color = fill_color

        self.pause_text = fonts.get(30).render("[PAUSE]", True, (255, 255, 255))
        self.exit_cin_text = fonts.get(20).render("Quitter la cinématique", True, (255, 255, 255))

        self.exit_ticks = 0.0
        self.MAX_EXIT_TICKS = 2.0

    def is_ended(self):
        return self.max_timeline <= self.ticks

    def update(self, delta: float) -> None:
        """
        Propriétés passées en arguments : - frequence : Horloge du moteur de jeux ; Permet d'accéder au nombre
        d'images par secondes, le nombre de ticks etc... - delta: un nombre exprimant le temps écoulé entre la
        dernière mise à jour et la mise à jour présente ; Bien souvent un nombre très faible (0.009 par exemple).
        """
        # Si la cinématique est finie, alors on ne va pas plus loin
        if self.is_ended():
            return

        if not self.pause:
            # La cinématique n'est pas en pause
            self.ticks += delta

        keys = pygame.key.get_pressed()
        # Vérifie si on doit quitter la cinématique
        if keys[pygame.K_e]:
            # Cet attribut exprime le temps pendant lequel la touche `e` (quitter) est pressée en secondes
            self.exit_ticks += delta

        if not keys[pygame.K_e] and self.exit_ticks != 0:
            # Si on n'appuie plus sur la touche `e`, alors on réinitialise le compteur
            self.exit_ticks = 0
        elif self.MAX_EXIT_TICKS <= self.exit_ticks:
            # On met les ticks au dela du maximum pour quitter la cinématique
            self.ticks = self.max_timeline + 1.0

    def key_down(self, event: pygame.event.Event):
        # Active/Désactive la pause de la cinématique
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
            self.pause = not self.pause

    def draw(self, screen: pygame.Surface) -> None:
        # Si la cinématique est terminée, on ne dessine rien, car c'est inutile
        if self.is_ended():
            return

        # Fond en noir :D
        if self.fill:
            screen.fill(self.fill_color)

        # Décalage de l'image pour les animations verticales des fonds
        delta = self.ticks * 20

        # Nous dessinons les images de fonds
        for asset in self.assets:
            if asset.is_middled(self.ticks):
                asset.draw(
                    screen,
                    delta
                )

        # Puis les textes...
        for text in self.texts:
            if text.is_middled(self.ticks):
                text.draw(screen)

        if self.pause or self.exit_ticks != 0:
            # On ajoute le fond si la pause est activée
            back_surface = pygame.Surface(screen.get_size())
            back_surface.set_alpha(191)  # 75% opaque
            back_surface.fill((0, 0, 0))

            screen.blit(back_surface, (0, 0))

        if self.pause:
            # Si la pause est activée, on rajoute un texte "[PAUSE]"
            screen.blit(
                self.pause_text,
                (
                    screen.get_width() // 2 - (self.pause_text.get_width() // 2),
                    screen.get_height() // 2 - (self.pause_text.get_height() // 2),
                )
            )

        if self.exit_ticks != 0:
            # On essaie de quitter la cinématique, alors on dessine l'animation
            # Texte "Quitter la cinématique"
            screen.blit(
                self.exit_cin_text,
                (
                    screen.get_width() - self.exit_cin_text.get_width() - 100,
                    screen.get_height() - self.exit_cin_text.get_height() - 100,
                )
            )
            # Rectangle correspondant au temps pendant lequel la touche `e` est appuyée
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (
                    screen.get_width() - self.exit_cin_text.get_width() - 100,
                    screen.get_height() - self.exit_cin_text.get_height() - 65,
                    floor(self.exit_cin_text.get_width() * (self.exit_ticks / self.MAX_EXIT_TICKS)),
                    7
                )
            )
