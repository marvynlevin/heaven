import pygame
from math import *
from typing import List, Tuple
from enum import Enum
from constants import DRAW_DEBUG_INFOS

from modules.assets import Assets
from entities.player import Player
from modules.fonts import fonts


class UiAssets(Assets):
    """
    Cette class permet de stocker les assets de l'interface utilisateur
    Voir `mod/assets.py`
    """

    def __init__(self) -> None:
        super().__init__()
        self.assets = {
            "inventory": pygame.image.load("assets/ui/inventory.png").convert_alpha(),
        }

    def get(self, key: str) -> pygame.Surface:
        if key in self.assets.keys():
            return self.assets[key]


class UiDrawArguments:
    """
    Cette class permet de faire de l'encapsulation. Cela permet de demander en arguments d'une fonction cette class
    et d'avoir accès à tous les attributs déclarés dedans
    """

    def __init__(self, player: Player, assets: UiAssets, screen: pygame.Surface) -> None:
        self.player = player
        self.assets = assets
        self.screen = screen

    def get(self) -> Tuple[Player, UiAssets, pygame.Surface]:
        """
        Décapsule les données
        """
        return self.player, self.assets, self.screen


class Component:
    """
    Cette class est un marqueur primaire.
    Elle ne possède aucun attribut ni méthodes, mais permet de déclarer plusieurs class
    comme des `Components`, ce qui facilite le typage et améliore considérablement la stabilité
    du jeu
    """
    pass

    def draw(self, game):
        pass

    def update(self, frequence, player):
        pass


class GameMessageStyle(Enum):
    """
    Cet énumérateur déclare les différents styles de messages possibles
    """
    CLASSIC = 1

    def get_color(self) -> Tuple[int, int, int]:
        """
        Renvoi la couleur de ce style
        Par défaut, la couleur est un noir absolu (alias rgb(0,0,0))
        """
        if self == GameMessageStyle.CLASSIC:
            return 240, 240, 240
        else:
            return 0, 0, 0


class GameMessage(Component):
    """
    Cette class permet d'intégrer des messages dans l'interface
    """

    def __init__(self, text: str, relativeCoordinates: Tuple[int, int],
                 style: GameMessageStyle = GameMessageStyle.CLASSIC) -> None:
        """
        Créer un nouveau message grâce à un texte, des coordinates relatives et à un style
        [!] Les coordonnées relatives sont basées sur l'écran, pas sur la carte !
        """
        self.message = text
        self.coords = relativeCoordinates
        self.style = style

    def draw(self, game: UiDrawArguments):
        # Décapsulation des arguments
        player, assets, screen = game.get()

        # On génère les textes en remplaçant les arguments par des valeurs
        # Sont actuellement implémentés:
        # - `x` & `y`: coordonnées du joueur en pixels (nombres flottants)
        # - `fps`: nombre de mises à jour effectuées en une seconde
        text = fonts.get(20).render(
            self.message
            .replace("{fps}", str(floor(player.fps)))
            .replace("{x}", str(round(player.x)))
            .replace("{y}", str(round(player.y))),
            True,
            self.style.get_color()
        )

        # Dessine le texte aux coordonnées définies
        screen.blit(
            text,
            self.coords
        )

    def update(self, frequence: pygame.time.Clock, player: Player):
        pass


class UI:
    """
    Cette class est le cœur de l'interface utilisateur.
    Elle rassemble chaque message déclaré
    """

    def __init__(self) -> None:
        # Par défaut, il n'y a pas de component
        self.components: List[Component] = []

        # Si la constante `DRAW_DEBUG_INFOS` est vraie, on ajoute les fps avec les coordonnées du joueur
        if DRAW_DEBUG_INFOS:
            self.components.append(GameMessage("fps: {fps}; ({x}, {y})", (5, 5), GameMessageStyle.CLASSIC))

    def draw(self, game: UiDrawArguments) -> None:
        # On dessine chaque component
        for cmp in self.components:
            cmp.draw(game)

        # dessiner l'interface de l'inventaire
        if game.player.inventory_open:
            self.draw_inventory(game)

    @staticmethod
    def draw_inventory(game: UiDrawArguments):
        """
        Au stade experimental
        """
        player, assets, screen = game.get()
        asset = assets.get("inventory")
        if asset is None:
            return

        # On rajoute un fond légèrement noir
        back_surface = pygame.Surface(screen.get_size())
        back_surface.set_alpha(128)
        back_surface.fill((0, 0, 0))

        screen.blit(back_surface, (0, 0))

        # Dessiner l'emplacement de la case où seront les items        
        screen.blit(
            asset,
            (
                (screen.get_width() // 2) - (asset.get_width() // 2),
                (screen.get_height() // 2) - (asset.get_height() // 2)
            )
        )

    def update(self, frequence: pygame.time.Clock, player: Player):
        """
        On met à jour les messages et components
        """
        for cmp in self.components:
            cmp.update(frequence, player)
