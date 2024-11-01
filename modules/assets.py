import pygame


class Assets:
    """
    Cette class contient toutes les images.
    L'utilisation de cette class permet d'éviter de charger les images sur le coup en les conservant en mémoire
    """

    def __init__(self) -> None:
        # de base, l'attribut `assets` est un dictionnaire vide
        self.assets = {}

    def get(self, key: str) -> pygame.Surface:
        """
        Récupère une Surface pygame grace à une clé [!] Renvoie `None` si la clé n'est pas présente (typage
        impossible à cause d'une incompatibilité de versions entre windows 7 et windows 10)
        """
        if key in self.assets.keys():
            return self.assets[key]


# GameAssets est un enfant de la class `Assets`
# Les attributs
class GameAssets(Assets):
    def __init__(self) -> None:
        super().__init__()
        self.assets = {
            # Joueur avec ses animations

            "player_bottom": pygame.transform.scale(pygame.image.load("assets/player/kady/down_1.png", "player_bottom"),
                                                    (96, 96)).convert_alpha(),
            "player_bottom_0": pygame.transform.scale(
                pygame.image.load("assets/player/kady/down_0.png", "player_bottom"), (96, 96)).convert_alpha(),
            "player_bottom_1": pygame.transform.scale(
                pygame.image.load("assets/player/kady/down_1.png", "player_bottom_1"), (96, 96)).convert_alpha(),
            "player_bottom_2": pygame.transform.scale(
                pygame.image.load("assets/player/kady/down_2.png", "player_bottom_2"), (96, 96)).convert_alpha(),

            "player_top": pygame.transform.scale(pygame.image.load("assets/player/kady/top_1.png", "player_top"),
                                                 (96, 96)).convert_alpha(),
            "player_top_0": pygame.transform.scale(pygame.image.load("assets/player/kady/top_0.png", "player_top"),
                                                   (96, 96)).convert_alpha(),
            "player_top_1": pygame.transform.scale(pygame.image.load("assets/player/kady/top_1.png", "player_top_1"),
                                                   (96, 96)).convert_alpha(),
            "player_top_2": pygame.transform.scale(pygame.image.load("assets/player/kady/top_2.png", "player_top_2"),
                                                   (96, 96)).convert_alpha(),

            "player_left": pygame.transform.scale(pygame.image.load("assets/player/kady/left_1.png", "player_left"),
                                                  (96, 96)).convert_alpha(),
            "player_left_0": pygame.transform.scale(pygame.image.load("assets/player/kady/left_0.png", "player_left_1"),
                                                    (96, 96)).convert_alpha(),
            "player_left_1": pygame.transform.scale(pygame.image.load("assets/player/kady/left_1.png", "player_left_1"),
                                                    (96, 96)).convert_alpha(),
            "player_left_2": pygame.transform.scale(pygame.image.load("assets/player/kady/left_2.png", "player_left_2"),
                                                    (96, 96)).convert_alpha(),

            "player_right": pygame.transform.scale(pygame.image.load("assets/player/kady/right_1.png", "player_right"),
                                                   (96, 96)).convert_alpha(),
            "player_right_0": pygame.transform.scale(
                pygame.image.load("assets/player/kady/right_0.png", "player_right"), (96, 96)).convert_alpha(),
            "player_right_1": pygame.transform.scale(
                pygame.image.load("assets/player/kady/right_1.png", "player_right_1"), (96, 96)).convert_alpha(),
            "player_right_2": pygame.transform.scale(
                pygame.image.load("assets/player/kady/right_2.png", "player_right_2"), (96, 96)).convert_alpha(),
        }
