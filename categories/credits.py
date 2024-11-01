from constants import *
from modules.fonts import fonts

"""
Le système des crédits est très simple

Il se compose d'un ensemble de textes/images qui défilent du bas vers le haut de l'écran
"""


class Credits:
    """
    Cette class représente le système des crédits
    """

    def __init__(self) -> None:
        # Le delta (exprimé en secondes) permettra de décaler les textes et images au fur et à mesure
        self.delta = 0

        # Nous allons définir au préalable chaque texte et image avec la bonne police, la bonne taille et la bonne
        # couleur Quand le texte est trop long pour passer sur l'écran, nous allons utiliser des List où elles
        # contiendront les rendus des textes, il suffira alors de parcourir chaque texte à la suite puis de dessiner
        # chaque texte

        self.title = fonts.get(35).render("Merci d'avoir joué au jeu!", True, (255, 255, 255))

        self.artist = fonts.get(35).render("Artistes & Designer", True, (255, 255, 255))
        self.artist_desc = fonts.get(30).render("Tony Moretti - Marvyn Levin", True, (255, 255, 255))

        self.history = fonts.get(35).render("Histoire & Level Designing", True, (255, 255, 255))
        self.history_desc = fonts.get(30).render("Colin Cédric", True, (255, 255, 255))

        self.dev = fonts.get(35).render("Développement", True, (255, 255, 255))
        self.dev_desc = fonts.get(30).render("Colin Cédric - Tony Moretti - Marvyn Levin", True, (255, 255, 255))

        self.debug = fonts.get(35).render("Débogage", True, (255, 255, 255))
        self.debug_desc = fonts.get(30).render("Marvyn Levin - Colin Cédric - Tony Moretti", True, (255, 255, 255))

        self.test = fonts.get(35).render("Testeurs", True, (255, 255, 255))
        self.test_desc = []
        test_desc = ["Tony Moretti - Marvyn Levin - Angelo Bosetti", "Colin Cédric - Stephane Lhomme"]
        for t in test_desc:
            self.test_desc.append(fonts.get(30).render(t, True, (255, 255, 255)))

        self.copyrights = fonts.get(35).render("Copyrights", True, (255, 255, 255))
        self.copyrights_desc = []
        copyright_text = ["finalbossblues (timefantasy.net) - Szadi art", "craftpix.net"]
        for t in copyright_text:
            self.copyrights_desc.append(fonts.get(30).render(t, True, (255, 255, 255)))

        self.teaser = fonts.get(35).render("We will be back, WHY NOT in 3D...", True, (255, 255, 255))
        self.teaser2 = fonts.get(35).render("...be prepared...", True, (255, 255, 255))
        self.teaser3 = fonts.get(45).render("For the Unknown", True, (255, 255, 255))

        # Nous ne pouvons pas charger l'image pour le moment, car le module d'images de pygame
        # ne peut pas être initialisé au démarrage du programme
        self.logo: pygame.Surface = None

        self.exit = False

    def draw(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()

        # On multiplie par 80 le delta, car le delta s'exprime en secondes.
        # Les textes/images auront donc un déplacement de 80 pixels/s vers le haut
        delta = self.delta * 80

        # Tout remplir en nooiiiiiirrrrrrrrrrrr
        screen.fill((0, 0, 0))

        # La variable `delta` est un peu comme une timeline
        # Si elle est supérieure à 0, alors on peut dessiner le texte
        # sinon, cela signifie qu'il n'est pas encore visible

        # Alors, pour chaque texte/image, nous allons vérifier si le delta est > 0, si oui, ainsi, nous allons
        # dessiner ce dernier en le centrant sur la longueur, et avec pour `y` l'expression `screen_height - delta`
        # Et enfin, si oui, nous allons également soustraire la hauteur de ce dernier et un écart (75 pixels en
        # général) afin de ne pas superposer les textes/images

        # Titre
        if delta > 0:
            screen.blit(self.title, ((screen_width // 2) - (self.title.get_width() // 2), screen_height - delta))
            delta -= self.title.get_height() + 75

        # Logo
        if delta > 0:
            screen.blit(self.logo, ((screen_width // 2) - (self.logo.get_width() // 2), screen_height - delta))
            delta -= self.logo.get_height() + 75

        # Artistes
        if delta > 0:
            screen.blit(self.artist, ((screen_width // 2) - (self.artist.get_width() // 2), screen_height - delta))
            delta -= self.artist.get_height() + 18
        if delta > 0:
            screen.blit(self.artist_desc,
                        ((screen_width // 2) - (self.artist_desc.get_width() // 2), screen_height - delta))
            delta -= self.artist_desc.get_height() + 75

        # Histoire
        if delta > 0:
            screen.blit(self.history, ((screen_width // 2) - (self.history.get_width() // 2), screen_height - delta))
            delta -= self.history.get_height() + 18
        if delta > 0:
            screen.blit(self.history_desc,
                        ((screen_width // 2) - (self.history_desc.get_width() // 2), screen_height - delta))
            delta -= self.history_desc.get_height() + 75

        # Dev
        if delta > 0:
            screen.blit(self.dev, ((screen_width // 2) - (self.dev.get_width() // 2), screen_height - delta))
            delta -= self.dev.get_height() + 18
        if delta > 0:
            screen.blit(self.dev_desc, ((screen_width // 2) - (self.dev_desc.get_width() // 2), screen_height - delta))
            delta -= self.dev_desc.get_height() + 75

            # Debug
        if delta > 0:
            screen.blit(self.debug, ((screen_width // 2) - (self.debug.get_width() // 2), screen_height - delta))
            delta -= self.debug.get_height() + 18
        if delta > 0:
            screen.blit(self.debug_desc,
                        ((screen_width // 2) - (self.debug_desc.get_width() // 2), screen_height - delta))
            delta -= self.debug_desc.get_height() + 75

        # Tester
        if delta > 0:
            screen.blit(self.test, ((screen_width // 2) - (self.test.get_width() // 2), screen_height - delta))
            delta -= self.test.get_height() + 18
        # Comme `self.test_desc` est une list, nous parcourons chaque élément de cette list
        # et nous le dessinons si delta est > 0, tout en soustrayant delta de la longueur et 15 pixels d'écart
        for t in self.test_desc:
            if delta > 0:
                screen.blit(t, ((screen_width // 2) - (t.get_width() // 2), screen_height - delta))
                delta -= t.get_height() + 15

        # Pour l'écart entre la liste des testeurs et le titre "Copyright"
        delta -= 75

        # Copyrights
        if delta > 0:
            screen.blit(self.copyrights,
                        ((screen_width // 2) - (self.copyrights.get_width() // 2), screen_height - delta))
            delta -= self.copyrights.get_height() + 18
        # Idem que pour les testeurs
        for t in self.copyrights_desc:
            if delta > 0:
                screen.blit(t, ((screen_width // 2) - (t.get_width() // 2), screen_height - delta))
                delta -= t.get_height() + 15

        delta -= 310

        # Teaser
        if delta > 0:
            screen.blit(self.teaser, ((screen_width // 2) - (self.teaser.get_width() // 2), screen_height - delta))
            delta -= self.teaser.get_height() + 18
        if delta > 0:
            screen.blit(self.teaser2, ((screen_width // 2) - (self.teaser2.get_width() // 2), screen_height - delta))
            delta -= self.teaser2.get_height() + 380
        if delta > 0:
            screen.blit(self.teaser3, ((screen_width // 2) - (self.teaser3.get_width() // 2), screen_height - delta))
            delta -= self.teaser3.get_height()

        # Si le delta calculé est supérieur à la hauteur de l'écran, alors cela signifie que tous les textes/images
        # ont été dessinés et on atteint le haut On peut ainsi quitter les crédits
        if delta >= screen_height:
            self.exit = True

    def reset_options_interface(self):
        """
        Cette fonction permet de réinitialiser les crédits
        """
        self.delta = 0

    def update(self, delta: float, engine):
        # Nous ajoutons `delta` à l'attribut `delta`
        self.delta += delta

        # Si l'attribut `exit` est vrai, nous quittons la cinématique en redéfinissant la catégorie du menu à
        # "aucune" (No one)
        if self.exit:
            engine.menu.ctg_open = MenuCategories.NO_ONE


# Afin d'y accéder depuis plusieurs endroits, nous définissons une variable qui pourra être accédée
# de partout dans le code source
credits: Credits = Credits()
