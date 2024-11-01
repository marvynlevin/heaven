import pygame

"""
Ce module permet de charger les polices et de les rendre accessibles pour tout les modules du programme

Pour accéder aux polices, il suffira d'importer la variable `fonts` (définie tout en bas) puis d'utiliser la méthode 
`get` de la class `Fonts`"""


class Fonts:
    """
    Cette class représente le module
    """

    def __init__(self) -> None:
        # Par défaut, nous stockons l'attribut "fonts" comme un dictionnaire vide.
        # Nous utiliserons comme clé la taille de police et en valeur la police pour cette même taille
        self.fonts = {}

    def load(self, font_size: int) -> None:
        """
        Charge la police avec une taille spécifique
        Ne charge pas la police si elle est déjà chargée pour cette taille
        """
        assert type(font_size) == int and font_size > 0, "`size` doit être un nombre entier supérieur à 0"
        if not (font_size in self.fonts):
            self.fonts[font_size] = pygame.font.Font("./RetroGaming.ttf", font_size)

    def get(self, font_size: int) -> pygame.font.Font:
        """
        Renvoi la police si elle a été chargée à cette taille
        [!] Renvoi `None` si la police n'est pas chargée
        """
        assert type(font_size) == int and font_size > 0, "`size` doit être un nombre entier supérieur à 0"
        if font_size in self.fonts:
            return self.fonts[font_size]


fonts: Fonts = Fonts()

# On charge les tailles de polices qui seront utilisées
# Le chargement au lancement de python permet de s'assurer qu'il n'y aura aucune latence pendant le jeu
for size in [55, 50, 45, 40, 35, 30, 25, 20, 15]:
    fonts.load(size)
