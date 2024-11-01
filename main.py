import pygame

from modules import save

# Nous initialisons le système de polices
# avant d'importer des modules qui utilisent le système de polices :o
pygame.font.init()

from constants import *
from menu import Menu
from constants import GameStatus
from game import Game
from categories.credits import credits

"""

Le fonctionnement du jeu se base sur une boucle simple, exprimée en langage naturel par:

jeu -> vrai
tant que jeu:
    mettre_a_jour_jeu()
    dessiner_jeu()
    
En effet, nous allons alterner à l'infinie une boucle `... -> mise à jour -> dessin -> ...`
Afin de lire les divers évènements (fermeture de fenêtres, pression de touches etc...), nous allons également insérer
avant chaque mise à jour une boucle qui va récupérer les évènements reçus depuis la dernière mise à jour.

Un des concepts les plus utilisés dans ce jeu est le concept de `delta` Le delta est un nombre flottant qui 
correspond au nombre de secondes écoulées depuis la dernière mise à jour L'utilité est que le delta permet d'exprimer 
des valeurs en unité/s et d'être certains que, si le nombre de mises à jours fluctue beaucoup, nous n'auront pas de 
mouvements/animation saccadés. Par exemple, la vitesse du joueur est exprimé en pixels/s, et est multiplié par le 
delta quand il est en mouvement. Ce qui fait que, si nous avons 60 mises à jours/s et que d'un coup nous passons à 
127, alors les mouvements du joueur seront toujours fluides.

Le jeu est organisé en plusieurs dossiers: - `entities`: contient tout le code lié aux entities (joueur etc...) - 
`categories`: contient le code source des catégories disponibles dans les menus - `modules`: contient la logique du 
jeu (collisions, map, inventaires, save, interface etc...) - `map`: contient les fichiers utilisé pour concevoir la 
carte (Avec le logiciel Tiled) - `algo`: contient des algorithmes qui ont été utilisés pour le jeu - `assets`: 
contient les images utiles au jeu - `poubelle`: le nom est transparent; ce dossier contient tout les fichiers bazars 
qui n'ont pas été utilisés/ne sont pas utiles dans l'immédiat

"""


class GameEngine:
    """Le gestionnaire du jeu"""

    def __init__(self):
        """
        Nous définissons toutes les variables qui seront utiles au jeu
        Principalement :
        - status: GameStatus; Utilisé pour savoir si nous sommes dans le menu ou en jeux
        - running : bool ; Utilisé par la boucle du jeu (voir plus bas)
        - menu: Menu ; Une class utilisée pour gérer les mises à jour/interactions/le comportement/l'interface du
            menu à l'entrée du jeu
        - game : Game ; Contient le jeu, similaire à la class Menu
        - fullscreen : bool ; Définit si le jeu est en plein écran ou non (utilisé dans la fonction "key_down")
        - display:
        """
        self.frequence = None
        self.display = None
        self.fullscreen = None
        self.status = GameStatus.MENU
        self.running = True
        self.LAST_FRAME = 0

        self.setup()

        self.menu = Menu()
        self.game = Game(self.display)

        # Nous chargeons la sauvegarde de la configuration
        save.load_config()
        save.init_save_system()

        self.run()

    def setup(self):
        """
        Initialise pygame et les attributs associés
        """
        pygame.init()  # Initialisation de pygame
        pygame.font.init()  # Initialisation du module des polices
        pygame.mixer.init()  # Initialisation du module des musiques

        # Nous récupérons les dimensions du moniteur où est le jeu
        monitor_info = pygame.display.Info()

        # Par défaut, le jeu n'est pas en plein écran
        self.fullscreen = False
        # Nous initialisons la fenêtre avec les dimensions du moniteur et la capacité de modifier la taille de la 
        # fenêtre (RESIZABLE)
        self.display = pygame.display.set_mode((monitor_info.current_w, monitor_info.current_h), pygame.RESIZABLE,
                                               display=0)  # Créer la fenêtre du jeu

        # Nous définissons le nom
        pygame.display.set_caption("Heaven")
        pygame.display.set_icon(pygame.image.load("assets/icons/icon2.png"))
        # Nous lançons l'horloge du jeu qui sera utilisée pour réguler le nombre d'images par secondes et beaucoup 
        # d'autres choses
        self.frequence = pygame.time.Clock()

        # Voir `categories/credits.py:62:41`
        credits.logo = pygame.image.load("./assets/logo.png").convert_alpha()

    def draw(self):
        """
        Cette fonction correspond à l'état "dessiner" vu plus haut
        
        Selon la valeur de l'attribut `status`, nous allons demander au menu OU au jeu
        de dessiner ce dernier
        
        Par défaut, le fond est un noir absolu
        """
        if self.status == GameStatus.MENU:
            self.menu.draw(self.display)
        elif self.status == GameStatus.GAME:
            self.game.draw(self.display)
        else:
            self.display.fill((0, 0, 0))

    def update(self):
        """
        Cette fonction correspond à l'état "mettre à jour" vu plus haut
        
        Selon la valeur de l'attribut `status`, nous allons demander au menu OU au jeu
        de se mettre à jour
        """
        # Nous calculons le delta et préparons le terrain
        # pour calculer le delta de la mise à jour suivante
        t = pygame.time.get_ticks()
        delta = (t - self.LAST_FRAME) / 1000.0
        self.LAST_FRAME = t

        if self.status == GameStatus.MENU:
            self.menu.update(delta, self)
        elif self.status == GameStatus.GAME:
            self.game.update(self.frequence, delta)

    def exit(self):
        """
        Cette fonction est appelée quand nous quittons le jeu
        """
        self.running = False

    def events(self):
        """
        Cette fonction correspond à l'état "évènement" vu plus haut
        """
        # Nous parcourons chaque évènement reçu par pygame
        for event in pygame.event.get():
            # Si l'évènement est un SIGINT (équivalent de : kill le programme, "fermer la fenêtre" etc...)
            if event.type == pygame.QUIT:
                self.exit()

            # Si une touche est appuyée
            elif event.type == pygame.KEYDOWN:
                # Plein écran ou non
                # Le plein écran s'active/désactive avec la touche F11
                if event.key == pygame.K_F11:
                    if not self.fullscreen:
                        monitor_info = pygame.display.Info()

                        self.fullscreen = True
                        # Pour mettre à jour la fenêtre, nous devons la fermer et redéfinir les "flags" en ajoutant 
                        # `pygame.FULLSCREEN`
                        pygame.display.quit()
                        self.display = pygame.display.set_mode((monitor_info.current_w, monitor_info.current_h),
                                                               flags=pygame.RESIZABLE and pygame.FULLSCREEN, vsync=1)
                        pygame.display.init()
                    else:
                        monitor_info = pygame.display.Info()

                        self.fullscreen = False
                        pygame.display.quit()
                        # Pour mettre à jour la fenêtre, nous devons la fermer et redéfinir les "flags" en retirant 
                        # `pygame.FULLSCREEN`
                        self.display = pygame.display.set_mode((monitor_info.current_w, monitor_info.current_h),
                                                               flags=pygame.RESIZABLE, vsync=1)
                        pygame.display.init()

                # Sinon, nous envoyons l'évènement au menu ou au jeu selon l'attribut `status`
                if self.status == GameStatus.MENU:
                    self.menu.key_down(event, self)
                elif self.status == GameStatus.GAME:
                    self.game.key_down(event, self)

            elif event.type == pygame.VIDEORESIZE:
                # La fenêtre ne fait plus la même taille.
                # Il y a toute une explication détaillée dans le cahier des charges sur
                # pourquoi nous devons faire cela (bugs)
                self.game.map.zone_decals = self.display.get_size()

    def run(self):
        """
        Cette fonction est notre fameuse boucle
        """
        while self.running:
            self.events()
            self.update()

            self.draw()

            # Nous mettons à jour l'affichage
            pygame.display.update()

            # Nous précisons à pygame qu'il peut y avoir au maximum `TICKS_PER_SECONDS` mises à jour/s
            self.frequence.tick(TICKS_PER_SECONDS)

        print("Good bye!")

        save.save_configuration()


# On initialise le jeu !
engine = GameEngine()
