from constants import *
from typing import Tuple

from modules import save
from modules.fonts import fonts
from modules.sound import Sound

"""

Le menu des options est très simple

Il se compose de 4 touches pouvant être modifiées


Il permet également d'activer ou désactiver les musiques
et de pouvoir changer le volume du jeu et des différentes
catégories de sons

"""


class Options:
    """
    Cette class représente la catégorie des options
    """

    def __init__(self) -> None:
        # On pré-définis les textes pour optimiser l'exécution
        self.esc_to_close = fonts.get(20).render("[ECHAP] pour quitter ce menu", True, (240, 240, 240))
        self.dev_mode = fonts.get(20).render("Mode développeur", True, (240, 240, 240))

        # Ces attributs permettent de naviguer entre les pages des options et les différentes lignes de chaque page
        self.actual_page = 0  # La page actuelle
        self.MAX_PAGES = 2  # Le nombre de pages maximal
        self.row_selected = 0  # La ligne actuelle
        self.MAX_SELECTED = 4  # Le nombre maximum de lignes pour cette page

        # Cet attribut définis les délais entre deux lectures de touches
        # Pour que, si on reste appuyé sur la touche `UP`, nous puissions monter d'une ligne toutes les 0.2s (200 ms)
        self.key_cooldown = 0.2

        # Cet attribut permet de déclarer si nous pouvons changer de pages
        self.can_change_page = True

        # Ces attributs sont utilisés par le système de définition des touches
        self.change_key = False  # Si nous sommes en train de changer la touche pour une action
        self.changed_key_name: str = "None"  # Le nom de l'action, purement esthétique
        self.changed_key_binding: str = ""  # Le nom de l'action dans la base de donnée, pas touche.

        # Ces attributs sont utilisés par le système de modification du volume
        self.change_volume = False
        self.volume_key: str = ""  # Le nom du paramètre dans la base de donnée
        self.volume_name: str = "None"  # Le nom du paramètre qui sera affiché

        # mode développeur
        # Le fonctionnement de ce système est classé secret défense.
        self.show_dev_page = False
        self.DEV_KEYS = 0

        # Comme les options peuvent être accédées depuis le jeu ou dans le menu principal,
        # cet attribut permet de savoir dans ces deux menus si les options demandent à être quittés
        self.close = False

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

        # En cas de définition d'une touche,
        # on dessine ce menu
        if self.change_key:
            return self.draw_key_binding(screen)

        # Si nous sommes en train de changer le volume
        # alors, on dessine ce menu
        if self.change_volume:
            return self.draw_volume_change(screen)

        # Mode dev:
        if self.show_dev_page:
            screen.blit(
                self.dev_mode,
                (
                    screen_width - 145 - self.dev_mode.get_width(),
                    120
                )
            )

        # Le dessin de la page selon l'attribut `self.actual_page`
        if self.actual_page == 0:
            # Général (modification des touches) nous définissons un `x` et `y` qui correspondent à la coordonnée du
            # coin en haut à gauche de la ligne la plus haute Pour chaque ligne, nous ajoutant la variable
            # `OPTIONS_LINES_MARGIN` (exprimé en pixels) pour espacer les lignes
            x, y = 190, 190

            # Nous dessinons le titre
            title = fonts.get(30).render("Contrôle des touches", True, (255, 255, 255))
            screen.blit(title, (x, y))

            # Nous déplaçons les prochaines éléments sur l'axe y
            y += title.get_height() + 35

            self.controls(screen, (x, y), "Haut", KEYS_BINDINGS["up"], self.row_selected == 0)
            y += OPTIONS_LINES_MARGIN

            self.controls(screen, (x, y), "Droite", KEYS_BINDINGS["right"], self.row_selected == 1)
            y += OPTIONS_LINES_MARGIN

            self.controls(screen, (x, y), "Bas", KEYS_BINDINGS["down"], self.row_selected == 2)
            y += OPTIONS_LINES_MARGIN

            self.controls(screen, (x, y), "Gauche", KEYS_BINDINGS["left"], self.row_selected == 3)
            y += OPTIONS_LINES_MARGIN
        elif self.actual_page == 1:
            # Son (activation/désactivation) + modification des volumes
            x, y = 190, 190

            # Nous dessinons le titre
            title = fonts.get(30).render("Paramètres de son", True, (255, 255, 255))
            screen.blit(title, (x, y))

            # Nous déplaçons les prochaines éléments sur l'axe y
            y += title.get_height() + 35

            if SOUND_CONFIG["play"]:
                self.checkbox(screen, (x, y), "Activé", SOUND_CONFIG["play"], self.row_selected == 0)
            else:
                self.checkbox(screen, (x, y), "Désactivé", SOUND_CONFIG["play"], self.row_selected == 0)

            y += OPTIONS_LINES_MARGIN

            self.sound_volume(screen, (x, y), "Son du jeu", SOUND_CONFIG["global"], self.row_selected == 1)
            y += OPTIONS_LINES_MARGIN

            self.sound_volume(screen, (x, y), "Musique", SOUND_CONFIG["music"], self.row_selected == 2)
            y += OPTIONS_LINES_MARGIN

            self.sound_volume(screen, (x, y), "Joueur", SOUND_CONFIG["player"], self.row_selected == 3)
            y += OPTIONS_LINES_MARGIN

            self.sound_volume(screen, (x, y), "Effets", SOUND_CONFIG["effects"], self.row_selected == 4)
            y += OPTIONS_LINES_MARGIN

        # On dessine les points qui correspondent aux pages
        if self.show_dev_page:
            pygame.draw.circle(
                screen,
                self.get_option_page_pos_color(0),
                (
                    screen_width // 2 - 30,
                    screen_height - 122
                ),
                9
            )
            pygame.draw.circle(
                screen,
                self.get_option_page_pos_color(1),
                (
                    screen_width // 2,
                    screen_height - 122
                ),
                9
            )
            pygame.draw.circle(
                screen,
                self.get_option_page_pos_color(2),
                (
                    screen_width // 2 + 30,
                    screen_height - 122
                ),
                9
            )
        else:
            pygame.draw.circle(
                screen,
                self.get_option_page_pos_color(0),
                (
                    screen_width // 2 - 15,
                    screen_height - 122
                ),
                9
            )
            pygame.draw.circle(
                screen,
                self.get_option_page_pos_color(1),
                (
                    screen_width // 2 + 15,
                    screen_height - 122
                ),
                9
            )

    def draw_volume_change(self, screen: pygame.Surface):
        """
        Cette fonction dessine le menu de changement du volume
        """
        sw, sh = screen.get_size()
        # fond
        pygame.draw.rect(
            screen,
            (20, 20, 20),
            (
                200,
                200,
                sw - 400,
                sh - 400
            ),
            border_radius=25
        )

        # On dessine l'instruction pour quitter le menu
        esc_text = fonts.get(30).render(f"[ECHAP] pour annuler l'action", True, (255, 255, 255))
        screen.blit(esc_text, ((sw // 2) - (esc_text.get_width() // 2), sh - 250 - (esc_text.get_height())))

        # On dessine le nom du paramètre
        title = fonts.get(30).render(self.volume_name, True, (255, 255, 255))
        screen.blit(title, ((sw // 2) - (title.get_width() // 2), 275 + (title.get_height() // 2)))

        if not (self.volume_key in SOUND_CONFIG):
            # Il y a un problème,
            # on signale l'erreur
            error = fonts.get(35).render("Une erreur est survenue", True, (255, 255, 255))
            screen.blit(error, ((sw // 2) - (error.get_width() // 2), (sh // 2) - (error.get_height() // 2)))
            # On ne doit pas aller plus loin
            return

        # On calcule le pourcentage 
        percent = SOUND_CONFIG[self.volume_key]

        # On dessine le pourcentage
        rendered_percent = fonts.get(25).render(
            f"{round(SOUND_CONFIG[self.volume_key], 0)}%",
            True,
            (255, 255, 255)
        )
        screen.blit(rendered_percent, (
            (sw // 2) - (rendered_percent.get_width() // 2), (sh // 2) - (rendered_percent.get_height() // 2) - 50))

        # On dessine le fond de la barre de progression
        bar_width = 800
        bar_height = 20

        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (
                (sw // 2) - (bar_width // 2),
                (sh // 2) + 50,
                bar_width,
                bar_height
            )
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                (sw // 2) - (bar_width // 2),
                (sh // 2) + 50,
                bar_width * (percent / 100.0),
                bar_height
            )
        )

    def draw_key_binding(self, screen: pygame.Surface):
        """
        Cette fonction dessine le menu quand nous changeons une touche
        """
        sw, sh = screen.get_size()
        # fond
        pygame.draw.rect(
            screen,
            (20, 20, 20),
            (
                200,
                200,
                sw - 400,
                sh - 400
            ),
            border_radius=25
        )

        # Nous dessinons les deux textes
        press_text = fonts.get(30).render(f"Changer la touche liée à l'action '{self.changed_key_name}'", True,
                                          (255, 255, 255))
        screen.blit(press_text, ((sw // 2) - (press_text.get_width() // 2), (sh // 2) - (press_text.get_height())))

        esc_text = fonts.get(30).render(f"[ECHAP] pour annuler l'action", True, (255, 255, 255))
        screen.blit(esc_text, ((sw // 2) - (esc_text.get_width() // 2), sh - 250 - (esc_text.get_height())))

    def get_option_page_pos_color(self, page: int) -> Tuple[int, int, int]:
        """
        Permet d'obtenir la couleur de la page si elle est sélectionnée ou non
        """
        if self.actual_page == page:
            return 230, 230, 230
        else:
            return 90, 90, 90

    @staticmethod
    def controls(screen: pygame.Surface, coords: Tuple[int, int], control: str, actual: pygame.key.key_code,
                 selected: bool):
        """
        Cette fonction permet de dessiner la ligne aux coordonnées (x, y), en sachant que cette ligne
        permet de lier une action à une touche
        """
        height = 32
        x, y = coords
        # Si la catégorie est sélectionnée, nous dessinons un point afin de montrer qu'elle est sélectionnée
        if selected:
            pygame.draw.circle(screen, (255, 255, 255), (x, y + (height // 2) + 3), radius=4)

        # Nous dessinons le nom de l'action
        name = fonts.get(25).render(control, True, (255, 255, 255))
        screen.blit(name, (x + 20, y + 4))
        x += 20 + 200

        # Nous dessinons le nom de la touche liée à cette action
        binded_key = fonts.get(25).render(f"{pygame.key.name(actual)}", True, (255, 255, 255))
        screen.blit(binded_key, (x, y + 4))

    @staticmethod
    def checkbox(screen: pygame.Surface, coords: Tuple[int, int], name: str, actual: bool, selected: bool):
        """
        Cette fonction permet de dessiner une case à cocher (checkbox) aux coordonnées (x,y)
        """
        height = 32
        x, y = coords
        x += 12
        # Si la catégorie est sélectionnée, nous dessinons un point afin de montrer qu'elle est sélectionnée
        if selected:
            pygame.draw.circle(screen, (255, 255, 255), (x, y + (height // 2) + 3), radius=4)

        x += 50
        # Nous dessinons les bords de la case :
        pygame.draw.circle(screen, (255, 255, 255), (x, y + (height // 2) + 3), radius=12)
        pygame.draw.circle(screen, (0, 0, 0), (x, y + (height // 2) + 3), radius=10)
        if actual:
            pygame.draw.circle(screen, (255, 255, 255), (x, y + (height // 2) + 3), radius=5)

        # Nous dessinons le nom
        x += 108
        box_name = fonts.get(25).render(name, True, (255, 255, 255))
        screen.blit(box_name, (x, y + 4))

    @staticmethod
    def sound_volume(screen: pygame.Surface, coords: Tuple[int, int], name: str, actual: float, selected: bool):
        """
        Cette fonction permet de dessiner la ligne qui permettra de changer le volume
        """
        height = 32
        x, y = coords
        # Si la catégorie est sélectionnée, nous dessinons un point afin de montrer qu'elle est sélectionnée
        if selected:
            pygame.draw.circle(screen, (255, 255, 255), (x, y + (height // 2) + 3), radius=4)

        x += 50
        # On dessine le niveau actuel
        volume = fonts.get(25).render(f"{round(actual)}%", True, (255, 255, 255))
        screen.blit(volume, (x, y + 4))

        x += 120

        # On dessine le nom
        rendered_name = fonts.get(25).render(name, True, (255, 255, 255))
        screen.blit(rendered_name, (x, y + 4))

    def reset_options_interface(self):
        """
        Cette fonction permet de réinitialiser cette catégorie quand nous la quittons
        """
        self.actual_page = 0
        self.row_selected = 0

        self.change_key = False
        self.changed_key_name: str = "None"
        self.changed_key_binding: str = ""

        self.change_volume = False
        self.volume_key = ""
        self.volume_name = "None"

        self.key_cooldown = 0.2
        self.close = False

    def update(self, delta: float):
        """
        Cette fonction est appelée à chaque mise à jour
        """
        keys = pygame.key.get_pressed()
        # Si les touches H, E, A, V et N (pour "Heaven") sont pressées simultanément, nous activons le mode développeur
        if (not self.show_dev_page) and (
                keys[pygame.K_h] and keys[pygame.K_e] and keys[pygame.K_a] and keys[pygame.K_v] and keys[pygame.K_n]):
            self.show_dev_page = True
            self.MAX_PAGES += 1

        # Si le cooldown de lecture des touches est inférieur ou nul, alors nous pouvons lire les touches
        if self.key_cooldown <= 0:
            # Nous redéfinissons le cooldown des touches
            self.key_cooldown = 0.2
            # Si le menu de changement de touche n'est pas activé et que "ENTRÉE" ou "ESPACE" est pressé,
            # nous entrons dans le menu de modification d'une touche
            if (not self.change_key) and (not self.change_volume) and (
                    keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and (
                    0 <= self.row_selected <= 3) and (self.actual_page == 0):
                self.change_key = True
                # On regarde la ligne sélectionnée pour savoir quelle est l'action
                match self.row_selected:
                    case 0:
                        self.changed_key_name = "Up"
                        self.changed_key_binding = "up"
                    case 1:
                        self.changed_key_name = "Right"
                        self.changed_key_binding = "right"
                    case 2:
                        self.changed_key_name = "Down"
                        self.changed_key_binding = "down"
                    case 3:
                        self.changed_key_name = "Left"
                        self.changed_key_binding = "left"
            # Si le menu de changement du volume n'est pas activé et que "ENTREE" ou "ESPACE" est pressé,
            # nous entrons dans le menu de modification du volume
            if not self.change_volume and (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and (
                    1 <= self.row_selected <= 4) and (self.actual_page == 1):
                self.change_volume = True
                match self.row_selected:
                    case 1:
                        self.volume_key = "global"
                        self.volume_name = "Volume global"
                    case 2:
                        self.volume_key = "music"
                        self.volume_name = "Volume de la musique"
                    case 3:
                        self.volume_key = "player"
                        self.volume_name = "Volume de(s) joueur(s)"
                    case 4:
                        self.volume_key = "effects"
                        self.volume_name = "Volume des effets"
                return
            elif self.change_volume:
                # Le menu de modification du volume est ouvert
                if keys[pygame.K_z] or keys[pygame.K_UP] or keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    # On augmente le volume de 0.01 (1%)
                    if round(SOUND_CONFIG[self.volume_key], 2) < 100.0:
                        SOUND_CONFIG[self.volume_key] += 1
                        self.key_cooldown = 0.05
                elif keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[pygame.K_q] or keys[pygame.K_LEFT]:
                    # On diminue le volume de 0.01 (1%)
                    if round(SOUND_CONFIG[self.volume_key], 2) > 0.0:
                        SOUND_CONFIG[self.volume_key] -= 1
                        self.key_cooldown = 0.05

                # Si le volume n'est pas bon, on va le corriger
                # Cela provient notamment des approximations liées aux nombres flottants
                if SOUND_CONFIG[self.volume_key] < 0.0:
                    SOUND_CONFIG[self.volume_key] = 0.0
                if SOUND_CONFIG[self.volume_key] > 100.0:
                    SOUND_CONFIG[self.volume_key] = 100.0
            # Si la touche "Z" ou "UP" est pressée et que nous ne sommes pas dans le menu de modification des touches,
            # nous passons à la ligne supérieure
            elif (keys[pygame.K_UP] or keys[pygame.K_z]) and (not self.change_key) and (not self.change_volume):
                self.row_selected = ((self.row_selected - 1) % self.MAX_SELECTED)
            # Si la touche "S" ou "DOWN" est pressée et que nous ne sommes pas dans le menu de modification des touches,
            # nous passons à la ligne inférieure
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (not self.change_key) and (not self.change_volume):
                self.row_selected = ((self.row_selected + 1) % self.MAX_SELECTED)

        elif self.key_cooldown > 0:
            # Sinon, nous ajoutons `delta` à l'attribut `key_cooldown` afin de réduire le temps avant la prochaine
            # lecture des touches
            self.key_cooldown -= delta

    def key_down(self, event, sound: Sound):
        # Une touche a été pressée, nous réinitialisons le cooldown
        self.key_cooldown = 0

        # Nous vérifions si le menu de modifications des touches est actif
        if self.change_key:
            # Ensuite, nous regardons si :
            # - la touche pressée n'est pas déjà liée à une autre action OU ele est identique à l'action sélectionnée
            # - la touche pressée n'est pas "ENTRÉE" ou "ESPACE"
            if (not (event.key in KEYS_BINDINGS.values()) or event.key == KEYS_BINDINGS[self.changed_key_binding]) and (
                    not (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE)):
                # Si la touche n'est pas "ECHAP", alors l'utilisateur n'a pas souhaité quitter ce menu
                # donc nous pouvons définir la nouvelle touche associée à l'action sélectionnée
                if event.key != pygame.K_ESCAPE:
                    KEYS_BINDINGS[self.changed_key_binding] = event.key
                # Nous réinitialisons les attributs liés au système de modification des touches
                self.change_key = False
                self.changed_key_name: str = "None"
                self.changed_key_binding: str = ""
                self.key_cooldown = 0.2
                return

        if self.change_volume:
            if event.key == pygame.K_ESCAPE:

                # On met à jour le volume de chaque musique
                sound.update_volumes()

                # On réinitialise tout
                self.change_volume = False
                self.volume_key: str = ""
                self.volume_name: str = "None"
                self.key_cooldown = 0.2
                return
            elif event.key in [pygame.K_z, pygame.K_UP, pygame.K_d, pygame.K_RIGHT]:
                # On augmente le volume de 0.01 (1%)
                if round(SOUND_CONFIG[self.volume_key], 2) < 100.0:
                    SOUND_CONFIG[self.volume_key] += 1
                    self.key_cooldown = 0.4
            elif event.key in [pygame.K_s, pygame.K_DOWN, pygame.K_q, pygame.K_LEFT]:
                # On diminue le volume de 0.01 (1%)
                if round(SOUND_CONFIG[self.volume_key], 2) > 0.0:
                    SOUND_CONFIG[self.volume_key] -= 1
                    self.key_cooldown = 0.4

        # Censored by the secret service :D
        if (not self.show_dev_page) and event.key == pygame.K_t and (not self.change_key) and (not self.change_volume):
            self.DEV_KEYS += 1
            if self.DEV_KEYS >= 5:
                self.show_dev_page = True
                self.MAX_PAGES += 1

        # Pour la configuration du son
        if self.actual_page == 1 and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
            if self.row_selected == 0:
                # C'est la case pour activer/désactiver le son
                SOUND_CONFIG["play"] = not SOUND_CONFIG["play"]

        # Changement de pages
        if self.can_change_page and ((event.key == pygame.K_a) or (event.key == pygame.K_LEFT)) and (
                not self.change_key) and (not self.change_volume):
            # changement de page vers la gauche si la touche "A" ou "LEFT" est pressée
            self.actual_page = (self.actual_page - 1) % self.MAX_PAGES
            # Si la page est la deuxième, soit le son, on incrémente de 1 le nombre de rows
            if self.actual_page == 1:
                self.MAX_SELECTED = 5
            else:
                self.MAX_SELECTED = 4
        elif self.can_change_page and (
                (event.key == pygame.K_e) or (event.key == pygame.K_RIGHT)) and (not self.change_key) and (
                not self.change_volume):
            # changement de page vers la droite si la touche "E" ou "RIGHT" est pressée
            self.actual_page = (self.actual_page + 1 + self.MAX_PAGES) % self.MAX_PAGES
            # Si la page est la deuxième, soit le son, on incrémente de 1 le nombre de rows
            if self.actual_page == 1:
                self.MAX_SELECTED = 5
            else:
                self.MAX_SELECTED = 4
        elif event.key == pygame.K_ESCAPE and (not self.change_key) and (not self.change_volume):
            # Si la touche est "ECHAP" et que nous ne sommes pas dans le menu de modification d'une touche ou du volume, 
            # on peut alors quitter les options
            self.close = True
            save.save_configuration()


# Afin d'y accéder depuis plusieurs endroits, nous définissons une variable qui pourra être accédée
# de partout dans le code source
options: Options = Options()
