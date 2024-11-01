# Nous importons BEAUCOUP de choses
import datetime

from entities.parent import *
from modules import save

from modules.map import *
from modules.camera import *
from modules.save import load_save, saves, GameSave
from modules.inventory import Wood
from modules.assets import GameAssets
from modules.cinematic import Cinematic, CinematicAsset, CinematicID, CinematicText, Position
from modules.sound import Sound, SoundsId, calc_sound_volume
from modules.ui import *
from modules.fonts import fonts
from modules.achievments import AchievementsID, achievements

from categories.options import options
from categories.success import success


#
#
#       GAME
#
#


class Game:
    """
    Cette class représente le jeu en lui-même
    """

    def __init__(self, screen: pygame.Surface) -> None:
        # Nous déclarons la carte, la caméra, le système de musique, les assets du jeu et les assets de l'interface
        self.map = load_save()  # Voir `modules/save.py`
        self.camera = Camera()
        self.assets = GameAssets()  # Voir `modules/assets.py`
        self.ui_assets = UiAssets()  # Voir `modules/ui.py`
        self.music = Sound()  # Voir `modules/sound.py`

        # On charge quelques musiques :
        self.music.load_sound(SoundsId.TEST, "assets/sounds/test.ogg")
        self.music.load_sound(SoundsId.CRN_FTP_1, "assets/sounds/crunchy-footsteps-1.ogg")
        self.music.load_sound(SoundsId.CRN_FTP_2, "assets/sounds/crunchy-footsteps-2.ogg")
        self.music.load_sound(SoundsId.CRN_FTP_3, "assets/sounds/crunchy-footsteps-3.ogg")
        self.music.load_sound(SoundsId.CRN_FTP_4, "assets/sounds/crunchy-footsteps-4.ogg")
        self.music.load_sound(SoundsId.CRN_FTP_5, "assets/sounds/crunchy-footsteps-5.ogg")
        self.music.load_sound(SoundsId.CRN_FTP_6, "assets/sounds/crunchy-footsteps-6.ogg")
        self.music.load_sound(SoundsId.CRN_FTP_7, "assets/sounds/crunchy-footsteps-7.ogg")

        # Le fameux bug du décalage quand on redimensionne la fenêtre
        self.map.zone_decals = screen.get_size()
        self.map.DEFAULT_ZONE_DECALS = screen.get_size()

        # Blep
        self.player = Player()

        # On stock l'identifiant de la partie
        self.save_id = 1

        # On va détermine le meilleur identifiant possible :
        saves.update()
        # On récupère les identifiants déjà utilisés
        already_used = [int(id) for id in saves.saves.keys()]
        # On va incrémenter l'identifiant de 1 tant que l'id est prise
        while self.save_id in already_used:
            self.save_id += 1

        # On enregistre la nouvelle sauvegarde
        saves.saves[self.save_id] = GameSave(
            {"player_coords": [self.player.x, self.player.y], "date": datetime.datetime.now()},
            self.save_id,
            os.path.join(SAVE_DIR, str(self.save_id) + ".json"),
            opened=True
        )

        saves.save(self.save_id, self)

        # On enregistre la date de la dernière sauvegarde
        self.last_save = datetime.datetime.now()

        # Non implémenté.
        self.player.inventory.add_item(Wood())

        # Nous initialisons l'interface de l'utilisateur
        self.ui = UI()  # Voir `modules/ui.py`

        # Menu affiché quand on appuie sur [ECHAP]
        self.is_escaped = False  # Si le menu de pause est affiché

        self.esc_menu_ctg = 0  # Le numéro de la catégorie ouverte
        self.space_between = 75  # Espace entre les catégories
        self.key_cooldown = 0.2  # Cooldown des touches, exprimé en secondes
        self.esc_menu_opened = False  # Si une catégorie est ouverte

        # Gestion des cinématiques
        # Voir `modules/cinematic.py`
        self.cinematics = {
            CinematicID.BEGINNING: Cinematic(
                [
                    CinematicAsset(
                        "test",
                        pygame.image.load("assets/ui/10.png"),
                        0,
                        19,
                        True,
                        (0, 0)
                    )
                ],
                [
                    CinematicText(
                        "1",
                        fonts.get(45).render("Elle était tout pour moi...", True, (0, 0, 0)),
                        0.5 - 0.15,
                        4.5 + 0.15,
                        center=True,
                        coords=(0, 100),
                        position=Position.BOTTOM
                    ),
                    CinematicText(
                        "2",
                        fonts.get(45).render("...jusqu'à ce moment.", True, (0, 0, 0)),
                        4.5 - 0.15 + 1,
                        9 + 0.15 + 1,
                        center=True,
                        coords=(0, 100),
                        position=Position.BOTTOM
                    ),
                    CinematicText(
                        "3",
                        fonts.get(45).render("Kady, me voilà.", True, (0, 0, 0)),
                        9 + 0.15 + 2,
                        14 + 0.15 + 2,
                        center=True,
                        coords=(0, 100),
                        position=Position.BOTTOM
                    )
                ],
                19
            )
        }

        # On déclare que la cinématique de début joue
        self.actual_cinematic = CinematicID.BEGINNING

        # Par défaut, nous allons joueur la cinématique "BEGINNING"
        self.run_cinematic = True

    def draw_esc_menu(self, screen: pygame.Surface) -> None:
        """
        Dessine le menu quand le jeu est en pause
        """

        # S'il n'est pas ouvert, on arrête tout de suite
        if not self.is_escaped:
            return

        # On rajoute un fond légèrement noir
        back_surface = pygame.Surface(screen.get_size())
        back_surface.set_alpha(191)  # 75% opaque

        back_surface.fill((0, 0, 0))

        screen.blit(back_surface, (0, 0))

        # On dessine les catégories suivantes :
        # - Retour en jeu
        # - Options
        # - Succès
        # - Quitter la partie
        # - Quitter le jeu

        # Le fonctionnement est similaire à `menu.py`

        (screen_width, screen_height) = screen.get_size()

        # [PAUSE]
        pause_top_text = fonts.get(25).render("[PAUSE]", True, (240, 240, 240))
        screen.blit(pause_top_text,
                    (floor((screen_width // 2) - (pause_top_text.get_width() // 2)), floor(self.space_between)))

        # Retour en jeu
        if self.esc_menu_ctg == 0:
            return_in_game = fonts.get(45).render("Retour en jeu", True, (179, 91, 110))
            screen.blit(return_in_game, (floor(screen_width // 2) - (return_in_game.get_width() // 2),
                                         floor(screen_height // 2) - self.space_between * 2.5))
        else:
            return_in_game = fonts.get(40).render("Retour en jeu", True, (255, 255, 255))
            screen.blit(return_in_game, (floor(screen_width // 2) - (return_in_game.get_width() // 2),
                                         floor(screen_height // 2) - self.space_between * 2.5))

        # Options
        if self.esc_menu_ctg == 1:
            opt_ctg = fonts.get(45).render("Options", True, (179, 91, 110))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2),
                                  floor(screen_height // 2) - self.space_between * 1.5))
        else:
            opt_ctg = fonts.get(40).render("Options", True, (255, 255, 255))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2),
                                  floor(screen_height // 2) - self.space_between * 1.5))

        # Contrôles
        if self.esc_menu_ctg == 2:
            cntrl_ctg = fonts.get(45).render("Succès", True, (179, 91, 110))
            screen.blit(cntrl_ctg, (floor(screen_width // 2) - (cntrl_ctg.get_width() // 2),
                                    floor(screen_height // 2) - self.space_between * 0.5))
        else:
            cntrl_ctg = fonts.get(40).render("Succès", True, (255, 255, 255))
            screen.blit(cntrl_ctg, (floor(screen_width // 2) - (cntrl_ctg.get_width() // 2),
                                    floor(screen_height // 2) - self.space_between * 0.5))

        # Quitter la partie
        if self.esc_menu_ctg == 3:
            opt_ctg = fonts.get(45).render("Quitter la partie", True, (179, 91, 110))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2),
                                  floor(screen_height // 2) + self.space_between * 0.5))
        else:
            opt_ctg = fonts.get(40).render("Quitter la partie", True, (255, 255, 255))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2),
                                  floor(screen_height // 2) + self.space_between * 0.5))

        # Quitter le jeu
        if self.esc_menu_ctg == 4:
            opt_ctg = fonts.get(45).render("Quitter le jeu", True, (179, 91, 110))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2),
                                  floor(screen_height // 2) + self.space_between * 1.5))
        else:
            opt_ctg = fonts.get(40).render("Quitter le jeu", True, (255, 255, 255))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2),
                                  floor(screen_height // 2) + self.space_between * 1.5))

    def draw(self, screen: pygame.Surface) -> None:
        """
        Cette fonction est appelée quand on doit dessiner le jeu
        """
        if self.run_cinematic:
            # Si une cinématique est en cours, on vérifie qu'elle ne soit pas terminée
            # et dans ce cas, on la dessine
            cin = self.cinematics[self.actual_cinematic]
            if not cin.is_ended():
                return cin.draw(screen)

        if self.esc_menu_opened:
            # Sinon, si le menu est ouvert, on regarde si une catégorie est ouverte
            # et si la catégorie "option" ou "succès" est ouverte, on dessine cette dernière
            match self.esc_menu_ctg:
                case 1:
                    return options.draw(screen)
                case 2:
                    return success.draw(screen)

        # Sinon, on remplis de noir
        screen.fill((0, 0, 0))

        # Puis, on dessine la carte
        self.map.draw(screen, self.assets, self.camera, self.player)
        # et par-dessus, l'interface de l'utilisateur
        self.ui.draw(UiDrawArguments(self.player, self.ui_assets, screen))

        # Et on termine par le menu de pause
        self.draw_esc_menu(screen)

        # Petit bonus
        screen.blit(
            fonts.get(15).render("En développement...", True, (255, 255, 255)),
            (20, screen.get_height() - 35)
        )

    def update(self, frequence: pygame.time.Clock, delta: float) -> None:
        """
        Cette fonction est appelée à chaque mise à jour
        """
        # On met à jour les succès
        self.update_success()

        # On vérifie si on doit auto sauvegarder
        if self.last_save.timestamp() + AUTO_SAVE_INTERVAL < datetime.datetime.now().timestamp():
            self.last_save = datetime.datetime.now()
            saves.save(self.save_id, self)

        # On synchronise les coordonnées du joueur avec les coordonnées de la caméra
        self.player.x = self.camera.x
        self.player.y = self.camera.y

        # Cinematic
        if self.run_cinematic:
            # Si une cinématique est en cours, on vérifie qu'elle ne soit pas terminée
            # et dans ce cas, on la met à jour
            cin = self.cinematics[self.actual_cinematic]
            if not cin.is_ended():
                # La cinématique est en cours
                return cin.update(delta)
            else:
                # On quitte la cinématique
                self.run_cinematic = False
                # On lance la musique du jeu
                self.music.play_sound(
                    SoundsId.TEST,
                    # On est multiple le coefficient du volume global par le coefficient
                    # du volume des musiques
                    volume=calc_sound_volume(SoundsId.TEST),
                    # On dit que le son se joue à l'infinie-
                    loops=-1
                )
                return

        # Si le menu des options est ouvert et qu'il demande à être fermé
        # alors, on le ferme et on le réinitialise
        if self.esc_menu_opened and options.close:
            options.reset_options_interface()
            self.esc_menu_opened = False
            save.save_configuration()
            return
        # Si le menu des succès est ouvert et qu'il demande à être fermé
        # alors, on le ferme et on le réinitialise
        if self.esc_menu_opened and success.close:
            success.reset_options_interface()
            self.esc_menu_opened = False
            return

        # Si le menu est ouvert et que les options sont ouvertes, on les met à jour
        if self.esc_menu_opened:
            match self.esc_menu_ctg:
                case 1:
                    return options.update(delta)

        # Si le menu "echap" est ouvert, le joueur ne doit pas se déplacer, alors :
        if not self.is_escaped:
            self.movements(delta)

        # On met à jour le joueur
        self.player.update(frequence, delta, self.music)
        # On met à jour l'interface
        self.ui.update(frequence, self.player)

        # On liste les clés pressées
        keys = pygame.key.get_pressed()
        # Si le cooldown de lecture des touches est finis et qu'aucune catégorie du menu est ouvert, alors...
        if self.key_cooldown <= 0 and not self.esc_menu_opened:
            self.key_cooldown = 0.2  # On réinitialise le cooldown
            # Si la touche "Z" ou "UP" est pressée, on monte la ligne sélectionnée de 1.
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.esc_menu_ctg = ((self.esc_menu_ctg - 1) % 5)
            # Si la touche "S" ou "DOWN" est pressée, on descend la ligne sélectionnée de 1.
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.esc_menu_ctg = ((self.esc_menu_ctg + 1) % 5)
        elif self.key_cooldown > 0:
            # Sinon, on réduit le cooldown de delta
            self.key_cooldown -= delta

    def key_down(self, event: pygame.event.Event, engine) -> None:
        """
        Cette fonction est appelée quand une touche est pressée
        """
        # Si une cinématique tourne, alors on lui envoie l'évènement
        if self.run_cinematic:
            cin = self.cinematics[self.actual_cinematic]
            if not cin.is_ended():
                return cin.key_down(event)

        # Si la catégorie "option" ou "succès" est ouverte, on lui envoie l'évènement
        if self.esc_menu_opened:
            match self.esc_menu_ctg:
                case 1:
                    return options.key_down(event, self.music)
                case 2:
                    return success.key_down(event)

        # Si la catégorie "options" est ouverte, on la ferme et on la réinitialise
        if self.esc_menu_opened and event.key == pygame.K_ESCAPE and not (
                self.esc_menu_opened and self.esc_menu_ctg == 2):
            self.esc_menu_opened = False
            options.reset_options_interface()

            return

        # Si la touche "ECHAP" est pressée et qu'aucune catégorie n'est ouverte, on ferme ou ouvre le menu de pause
        # et on retourne au jeu
        if event.key == pygame.K_ESCAPE and not self.esc_menu_opened:
            # On relance la musique
            if self.is_escaped:
                self.music.resume_all_sounds()
            else:
                self.music.pause_all_sounds()

            self.is_escaped = not self.is_escaped
            self.esc_menu_ctg = 0
        # -- Non implémenté:
        # elif (event.key == pygame.K_e) and (not self.is_escaped):
        #     self.player.inventory_open = not self.player.inventory_open

        # Si la touche "Z" ou "UP" est pressée, que le menu est ouvert et qu'aucune catégorie n'est ouverte,
        # on monte la ligne sélectionnée de 1.
        elif ((event.key == pygame.K_UP) or (event.key == pygame.K_z)) and self.is_escaped and not self.esc_menu_opened:
            self.key_cooldown = 0.2
            self.esc_menu_ctg = ((self.esc_menu_ctg - 1) % 5)
        # Si la touche "S" ou "DOWN" est pressée, que le menu est ouvert et qu'aucune catégorie n'est ouverte,
        # on descend la ligne sélectionnée de 1.
        elif ((event.key == pygame.K_DOWN) or (
                event.key == pygame.K_s)) and self.is_escaped and not self.esc_menu_opened:
            self.key_cooldown = 0.2
            self.esc_menu_ctg = ((self.esc_menu_ctg + 1) % 5)

        # Si la touche "ESPACE" ou "ENTRÉE" est pressée et que nous sommes dans le menu
        elif ((event.key == pygame.K_SPACE) or (event.key == pygame.K_RETURN)) and self.is_escaped:
            if self.esc_menu_ctg == 4:
                # On sauvegarde la partie
                saves.save(self.save_id, self)
                # Quitter le jeu
                engine.running = False
            elif self.esc_menu_ctg == 3:
                # Retour au menu
                engine.status = GameStatus.MENU
                self.esc_menu_ctg = False
                self.player.inventory_open = False

                # On sauvegarde la partie
                saves.save(self.save_id, self)
            elif self.esc_menu_ctg == 0:
                # Retour en jeux
                self.music.resume_all_sounds()
                self.is_escaped = not self.is_escaped
            elif self.esc_menu_ctg == 2:
                # Succès
                # On met à jour la liste des succès
                success.enter()
            
            if self.esc_menu_ctg == 1 or self.esc_menu_ctg == 2:
                # On déclare que la catégorie est ouverte
                self.esc_menu_opened = True
                # On met en pause la musique
                self.music.pause_all_sounds()

    def manage_collisions(self, vec: Tuple[int, int], movement: Movement) -> Tuple[int, int]:
        """
        Cette fonction gère les collisions
        
        Elle va vérifier s'il y a une collision à la future position du joueur
        
        S'il y a une collision, nous allons décomposer le mouvement de cette facon :
        - Si le mouvement se déplace sur x, on dit que le mouvement du joueur sur x pour ce moment est 0
        - Si le mouvement se déplace sûr y, on dit que le mouvement du joueur sur y pour ce moment est 0
        
        Cela permet que, s'il y a une collision à droite, mais que le joueur se déplace avec un mouvement TOP_RIGHT
        (diagonale), alors le joueur pourra toujours monter.
        """

        # Voir `modules/collisions.py`
        collisions = collisions_algo(self.map.actual_zone.collisions, self.player.x + (CASE_SIZE // 2) + vec[0],
                                     self.player.y + (CASE_SIZE // 2) + vec[1])

        # S'il n'y a pas de collisions, c'est réglé, on renvoie le vecteur tel qu'il a été reçu
        if not collisions:
            return vec

        # Sinon, on décompose le mouvement        
        if (movement in [Movement.UP, Movement.UP_LEFT, Movement.UP_RIGHT, Movement.BOTTOM, Movement.BOTTOM_LEFT,
                         Movement.BOTTOM_RIGHT]) and collisions:
            vec = (vec[0], 0)
        if (movement in [Movement.RIGHT, Movement.UP_RIGHT, Movement.BOTTOM_RIGHT, Movement.UP_LEFT, Movement.LEFT,
                         Movement.BOTTOM_LEFT]) and collisions:
            vec = (0, vec[1])

        return vec

    def movements(self, delta: float) -> None:
        """
        On vérifie chaque touche (z, q, s, d) pour connaitre le mouvement précis
        Les mouvements sont décrits par l'énumérateur `Movement`
        la vitesse du joueur est négative si :
        - il se déplace en haut
        - il se déplace à gauche
        la vitesse du joueur est positive si :
        - il se déplace en bas
        - il se déplace à droite

        Chaque mouvement est basé sur les touches liées dans `KEYS_BINDINGS` (voir `constants.py`)
        
        """
        keys = pygame.key.get_pressed()

        vec = (0, 0)
        movement = self.player.movement

        if keys[KEYS_BINDINGS["down"]] and keys[KEYS_BINDINGS["left"]] and (not keys[KEYS_BINDINGS["right"]]):
            # move bottom left
            vec = (self.camera.speed, -self.camera.speed)
            movement = Movement.BOTTOM_LEFT
        elif keys[KEYS_BINDINGS["down"]] and keys[KEYS_BINDINGS["right"]] and (not keys[KEYS_BINDINGS["left"]]):
            # move bottom right
            vec = (-self.camera.speed, -self.camera.speed)
            movement = Movement.BOTTOM_RIGHT
        elif keys[KEYS_BINDINGS["up"]] and keys[KEYS_BINDINGS["left"]] and (not keys[KEYS_BINDINGS["right"]]):
            # move up left
            vec = (self.camera.speed, self.camera.speed)
            movement = Movement.UP_LEFT
        elif keys[KEYS_BINDINGS["up"]] and keys[KEYS_BINDINGS["right"]] and (not keys[KEYS_BINDINGS["left"]]):
            # move up right
            vec = (-self.camera.speed, self.camera.speed)
            movement = Movement.UP_RIGHT
        elif keys[KEYS_BINDINGS["up"]] and (
                (not (keys[KEYS_BINDINGS["left"]] or keys[KEYS_BINDINGS["right"]] or keys[KEYS_BINDINGS["down"]])) or (
                (keys[KEYS_BINDINGS["left"]] and keys[KEYS_BINDINGS["right"]]) or keys[KEYS_BINDINGS["down"]])):
            # move only up
            vec = (0, self.camera.speed)
            movement = Movement.UP
        elif keys[KEYS_BINDINGS["left"]] and not (
                keys[KEYS_BINDINGS["up"]] or keys[KEYS_BINDINGS["down"]] or keys[KEYS_BINDINGS["right"]]):
            # move only left
            vec = (self.camera.speed, 0)
            movement = Movement.LEFT
        elif keys[KEYS_BINDINGS["right"]] and not (
                keys[KEYS_BINDINGS["up"]] or keys[KEYS_BINDINGS["down"]] or keys[KEYS_BINDINGS["left"]]):
            # move only right
            vec = (-self.camera.speed, 0)
            movement = Movement.RIGHT
        elif keys[KEYS_BINDINGS["down"]] and (
                (not (keys[KEYS_BINDINGS["left"]] or keys[KEYS_BINDINGS["right"]] or keys[KEYS_BINDINGS["down"]])) or (
                (keys[KEYS_BINDINGS["left"]] and keys[KEYS_BINDINGS["left"]]) or keys[KEYS_BINDINGS["down"]])):
            # move only bottom
            vec = (0, -self.camera.speed)
            movement = Movement.BOTTOM

        # S'il n'y a aucun changement de coordonnées et de mouvement, on arrête immédiatement
        if (self.player.movement == movement) and (vec == (0, 0)):
            return

        # Si le mouvement n'est pas que sur x ou y, on doit le normaliser
        # On applique alors le théorème de Pythagore
        if vec[0] != 0 and vec[1] != 0:
            # Hypothénus:
            hypo = sqrt(vec[0] ** 2 + vec[1] ** 2)
            # On calcul le ratio
            normalization_coeff = SPEED_NORMALIZE_SEUIL / hypo
            # On l'applique sur le vecteur
            vec = (vec[0] * normalization_coeff, vec[1] * normalization_coeff)

        # On décompose le mouvement du joueur
        # S'il y a un mouvement sur l'axe `x`, on déplace le joueur sur x
        decompose_x = determine_collision_move(movement, 0)
        if not (decompose_x is None):
            # On lui donne un vecteur qui est le résultat de l'algorithme de collisions
            # Voir la fonction `manage_collisions` pour plus de détails
            self.player.move(movement, self.manage_collisions((vec[0] * delta, 0), movement), self.camera, delta)

        # S'il y a un mouvement sur l'axe `y`, on déplace le joueur sur y
        decompose_y = determine_collision_move(movement, 1)
        if not (decompose_y is None):
            # On lui donne un vecteur qui est le résultat de l'algorithme de collisions
            # Voir la fonction `manage_collisions` pour plus de détails
            self.player.move(movement, self.manage_collisions((0, vec[1] * delta), movement), self.camera, delta)
    
    def update_success(self):
        """
        Cette fonction permet de mettre à jour les succès
        """

        # TODO
        # - Afficher une message pour avertir que un succès a été débloqué
        # - Ajouter les autres succès
        # - Sauvegarder les succès

        if not achievements.is_complete(AchievementsID.WALK_10000_STEPS) and self.player.foots >= 10000:
            achievements.complete(AchievementsID.WALK_10000_STEPS)
