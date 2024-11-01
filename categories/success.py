from constants import *
from modules.fonts import fonts
from modules.achievments import Achievement, achievements

"""
Ce fichier contient le menu des succès
"""


class Success:
    def __init__(self) -> None:
        self.esc_to_close = fonts.get(20).render("[ECHAP] pour quitter ce menu", True, (240, 240, 240))
        self.no_success = fonts.get(35).render("Aucune partie sauvegardée.", True, (240, 240, 240))

        # Comme les succès peuvent être accédés depuis le jeu ou dans le menu principal,
        # cet attribut permet de savoir dans ces deux menus si les succès demandent à être quittés
        self.close = False

        # On stocke la page actuelle
        self.actual_page = 0
        # On stocke le nombre maximal de pages
        self.MAX_PAGE = 0
        # On stocke le nombre maximal de lignes
        self.MAX_ROWS = 10

        # Cet attribut définis les délais entre deux lectures de touches
        # Pour que, si on reste appuyé sur la touche `UP`, nous puissions monter d'une ligne toutes les 0.2s (200 ms)
        self.key_cooldown = 0.2

        # On prépare le terrain pour afficher les succès
        self.success = []

    def enter(self):
        """
        Cette fonction est appelée quand nous entrons dans ce menu
        """
        # On met à jour la liste formatée des succès
        self.success = achievements.format(self.MAX_ROWS)
        
        # On met à jour le nombre maximal de pages et 
        # on réinitialise la page actuelle
        self.MAX_PAGE = len(self.success)
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

        # Message qu'aucun succès n'existe
        if len(self.success) < 1 or (self.actual_page > len(self.success) - 1) or len(self.success[self.actual_page]) < 1:
            screen.blit(
                self.no_success,
                (
                    (screen_width // 2) - (self.no_success.get_width() // 2),
                    (screen_height // 2) - (self.no_success.get_height() // 2),
                )
            )
            return
        
        actual_success = self.success[self.actual_page]

        x, y = 190, 190

        for i in range(0, len(actual_success)):
            # On appelle la méthode pour dessiner le succès
            self.draw_success(screen, actual_success[i], x, y)
            # On augmente `y` pour ne pas superposer les textes
            y += 108

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
    def draw_success(screen: pygame.Surface, achievment: Achievement, x: int, y: int):
        """
        Cette fonction permet de dessiner un succès sur l'écran
        """
        height = 108
        # On dessine une magnifique ligne
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (200, y, screen.get_width() - 400, 1)
        )

        x += 50

        color = (255, 255, 255)
        if not achievment.completed:
            color = (70, 70, 70)

        # On dessine le nom
        success_name = fonts.get(25).render(achievment.name, True, color)
        screen.blit(success_name, (x, y + ((height // 2) - success_name.get_height() // 2)))

        # puis la description
        success_desc = fonts.get(25).render(achievment.description, True, color)
        screen.blit(
            success_desc,
            (
                x + 25,
                y + ((height // 2) - success_name.get_height() // 2)
                    + success_name.get_height()
            )
        )
            
            
        # On dessine une seconde ligne
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (200, y + height, screen.get_width() - 400, 1)
        )




    def key_down(self, event):
        """
        Cette fonction se déclenche quand une touche est pressée
        """

        # si la touche `ECHAP` est pressée, nous quittons la catégorie
        if event.key == pygame.K_ESCAPE:
            self.close = True

    def reset_options_interface(self):
        """
        Cette fonction permet de réinitialiser cette catégorie quand nous la quittons
        """
        self.close = False


# Afin d'y accéder depuis plusieurs endroits, nous définissons une variable qui pourra être accédée
# de partout dans le code source
success: Success = Success()
