import datetime
from math import *
from constants import *
from categories.options import options
from categories.success import success
from categories.load import load
from categories.credits import credits
import modules.save as save
from constants import GameStatus
from entities.player import Player
from modules.camera import Camera
from modules.cinematic import CinematicID
from modules.fonts import fonts
from modules.map import ZoneType

MENU_SELECTED_COLOR = (0, 87, 168)  # (113, 6, 39)


class Menu:
    """
    Le menu principal du jeu
    """

    def __init__(self):
        # On a pré-définis le texte "Menu" pour optimiser pendant le runtime
        text = fonts.get(55).render("Menu", True, (240, 240, 240))
        self.text_surface = text.get_rect()

        self.category = 0
        self.space_between = 100  # Espace entre les catégories, en pixel
        self.key_cooldown = 0  # Utilisé pour détecter les touches à interval régulier

        # On définit la catégorie du menu ouverte
        self.ctg_open = MenuCategories.NO_ONE

        # On stocke le delta pour l'animation
        self.delta = 0

        # On définit le fond du menu
        self.old_background = pygame.image.load("assets/ui/menu.png").convert_alpha()
        self.background = pygame.image.load("assets/ui/cloud_2.png").convert_alpha()

    def draw_background(self, screen: pygame.Surface):
        """
        Dessine l'image de fond
        """
        # On calcule le décalage de l'image (delta, exprimé en pixels).
        # Ici, le décalage est de 20 pixels/s
        delta = self.delta * 20

        # On dessine une première fois l'image
        screen.blit(self.background, (0, 0))

        screen.blit(
            self.background,
            (
                delta % self.background.get_width(),
                0
            )
        )
        screen.blit(
            self.background,
            (
                (delta % self.background.get_width()) - self.background.get_width(),
                0
            )
        )
        # surface = pygame.transform.scale(self.old_background, screen.get_size())
        # screen.blit(surface, (0, 0))

    def draw(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        # Dessine le fond
        self.draw_background(screen)

        # Si une catégorie du menu est ouverte, on la dessine
        if self.ctg_open == MenuCategories.OPTIONS:
            return options.draw(screen)
        elif self.ctg_open == MenuCategories.SUCCESS:
            return success.draw(screen)
        elif self.ctg_open == MenuCategories.LOAD_GAME:
            return load.draw(screen)
        elif self.ctg_open == MenuCategories.CREDITS:
            return credits.draw(screen)

        # Sinon, on dessine les catégories disponibles Pour chaque catégorie, on vérifie si elle est sélectionnée
        # Seule une catégorie peut être sélectionnée et sera d'une couleur et taille différente L'espacement entre
        # les catégories utilise un rapport de proportionality sur l'axe vertical, avec pour centre le centre de
        # l'écran

        (display_width, display_height) = screen.get_size()

        if self.category == 0:
            new_game_ctg = fonts.get(55).render("Nouvelle partie", True, MENU_SELECTED_COLOR)
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) - self.space_between * 2.5 - (
                                               self.space_between // 2)))
        else:
            new_game_ctg = fonts.get(50).render("Nouvelle partie", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) - self.space_between * 2.5 - (
                                               self.space_between // 2)))

        if self.category == 1:
            new_game_ctg = fonts.get(55).render("Charger une partie", True, MENU_SELECTED_COLOR)
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) - self.space_between * 1.5 - (
                                               self.space_between // 2)))
        else:
            new_game_ctg = fonts.get(50).render("Charger une partie", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) - self.space_between * 1.5 - (
                                               self.space_between // 2)))

        if self.category == 2:
            new_game_ctg = fonts.get(55).render("Options", True, MENU_SELECTED_COLOR)
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) - self.space_between * 0.5 - (
                                               self.space_between // 2)))
        else:
            new_game_ctg = fonts.get(50).render("Options", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) - self.space_between * 0.5 - (
                                               self.space_between // 2)))

        if self.category == 3:
            new_game_ctg = fonts.get(55).render("Succès", True, MENU_SELECTED_COLOR)
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) + self.space_between * 0.5 - (
                                               self.space_between // 2)))
        else:
            new_game_ctg = fonts.get(50).render("Succès", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) + self.space_between * 0.5 - (
                                               self.space_between // 2)))

        if self.category == 4:
            new_game_ctg = fonts.get(55).render("Crédits", True, MENU_SELECTED_COLOR)
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) + self.space_between * 1.5 - (
                                               self.space_between // 2)))
        else:
            new_game_ctg = fonts.get(50).render("Crédits", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) + self.space_between * 1.5 - (
                                               self.space_between // 2)))

        if self.category == 5:
            new_game_ctg = fonts.get(55).render("Quitter", True, MENU_SELECTED_COLOR)
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) + self.space_between * 2.5 - (
                                               self.space_between // 2)))
        else:
            new_game_ctg = fonts.get(50).render("Quitter", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 2) + self.space_between * 2.5 - (
                                               self.space_between // 2)))

    def update(self, delta: float, engine):
        # On met à jour le delta
        self.delta += delta

        # Si le menu des options est ouvert et qu'il a son attribut `close` vrai,
        # alors on ferme le menu et on le réinitialise
        if self.ctg_open == MenuCategories.OPTIONS and options.close:
            options.reset_options_interface()
            self.ctg_open = MenuCategories.NO_ONE
            save.save_configuration()
            return
        # Si le menu des succès est ouvert et qu'il a son attribut `close` vrai,
        # alors on ferme le menu et on le réinitialise
        if self.ctg_open == MenuCategories.SUCCESS and success.close:
            success.reset_options_interface()
            self.ctg_open = MenuCategories.NO_ONE
            return

        # Si le menu des options ou les crédits sont ouverts, on les met à jour et on termine la fonction
        if self.ctg_open == MenuCategories.OPTIONS:
            return options.update(delta)
        elif self.ctg_open == MenuCategories.CREDITS:
            return credits.update(delta, engine)
        elif self.ctg_open == MenuCategories.LOAD_GAME:
            return load.update(delta)

        # Permet de lire les touches à interval régulier
        keys = pygame.key.get_pressed()
        if self.key_cooldown <= 0:
            self.key_cooldown = 0.25  # En secondes, correspond à (1/4) de secondes ou 250 ms
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                # On monte d'une catégorie
                self.category = ((self.category - 1) % 6)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                # On descend d'une catégorie
                self.category = ((self.category + 1) % 6)
        elif self.key_cooldown > 0:
            # Si le cooldown de lecture des touches n'est pas terminé, on décrémente de delta
            self.key_cooldown -= delta

    #
    #
    #       Control
    #
    #

    def options_control_key_down(self, event: pygame.event.Event):
        """
        Si la touche ECHAP est appuyée et qu'on a le menu des succès ou de chargement de partie ouvert,
        alors on le ferme et on le réinitialise
        """
        if event.key == pygame.K_ESCAPE:
            if self.ctg_open == MenuCategories.LOAD_GAME:
                load.reset_options_interface()
                self.ctg_open = MenuCategories.NO_ONE
            elif self.ctg_open == MenuCategories.SUCCESS:
                success.reset_options_interface()
                self.ctg_open = MenuCategories.NO_ONE

    def key_down(self, event: pygame.event.Event, engine):
        """
        Cette fonction est déclenchée à chaque fois qu'une touche est pressée (au moment où elle est appuyée)
        """

        # Si une catégorie est ouverte, on lui envoie l'évènement et on arrête la fonction ici
        if self.ctg_open == MenuCategories.OPTIONS:
            options.key_down(event, engine.game.music)
            self.options_control_key_down(event)
            return
        elif self.ctg_open == MenuCategories.SUCCESS:
            success.key_down(event)
            self.options_control_key_down(event)
        elif self.ctg_open == MenuCategories.LOAD_GAME:
            load.key_down(event, engine)
            self.options_control_key_down(event)
            return

        # On réinitialise le temps d'attente pour la lecture des touches
        self.key_cooldown = 0

        # Si la touche ENTRÉE ou ESPACE a été pressée, on regarde la catégorie et l'action associée
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.category == 0:
                # On réinitialise les données
                engine.game.player = Player()
                engine.game.camera = Camera()

                engine.game.music.stop_sounds()
                engine.game.esc_menu_opened = False
                engine.game.is_escaped = False
                engine.game.esc_menu_ctg = 0
                engine.game.map.actual_zone = engine.game.map.zones[ZoneType.START]

                # On va détermine le meilleur identifiant possible pour le fichier de sauvegarde :
                save.saves.update()
                # On récupère les identifiants déjà utilisés
                already_used = [int(id) for id in save.saves.saves.keys()]
                # On va incrémenter l'identifiant de 1 tant que l'id est prise
                while engine.game.save_id in already_used:
                    engine.game.save_id += 1

                # On enregistre la nouvelle sauvegarde
                save.saves.saves[engine.game.save_id] = save.GameSave(
                    {"player_coords": [engine.game.player.x, engine.game.player.y], "date": datetime.datetime.now()},
                    engine.game.save_id,
                    os.path.join(SAVE_DIR, str(engine.game.save_id) + ".json"),
                    opened=True
                )

                # On enregistre la date de la dernière sauvegarde
                engine.game.last_save = datetime.datetime.now()

                # On déclare que la cinématique de début joue
                engine.game.actual_cinematic = CinematicID.BEGINNING

                # Par défaut, nous allons joueur la cinématique "BEGINNING"
                engine.game.run_cinematic = True
                for cinematic in engine.game.cinematics.values():
                    cinematic.ticks = 0
                    cinematic.pause = False

                # Entrée dans le jeu
                engine.status = GameStatus.GAME
            elif self.category == 1:
                # Charger une partie
                self.ctg_open = MenuCategories.LOAD_GAME
                load.enter()
            elif self.category == 2:
                # Catégorie des options
                self.ctg_open = MenuCategories.OPTIONS
            elif self.category == 3:
                # Catégorie des succès
                self.ctg_open = MenuCategories.SUCCESS
                # On met à jour la liste des succès
                success.enter()
            elif self.category == 4:
                # Catégorie des crédits
                self.ctg_open = MenuCategories.CREDITS
            elif self.category == 5:
                # Quitter le jeu
                engine.exit()
