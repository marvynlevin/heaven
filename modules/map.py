from typing import Dict

from modules.assets import Assets
from modules.camera import *
from entities.player import Player
from modules.collisions import *

"""

    --- EXPLICATIONS ---
    
La carte est constituée de Zones
Chaque zone possède ses collisions, entities et couches

Une zone possède au minimum un fond, une image du fond de carte pour être précis.
Accompagné de ce fond, chaque zone possède aussi des "couches" qui sont des images superposées par dessus le fond
Cela permet de dessiner le joueur entre deux fonds.
"""


class ZoneType(Enum):
    """
    Cette class énumère les différentes zones possibles
    """
    START = 0


class Zone:
    """
    Cette class permet de définir une Zone
    
    [!] Les entities ne sont pas implémentées
    """

    def __init__(self,
                 map_background: pygame.Surface,  # Fond de la carte
                 layers=None,  # Les couches sous forme de tuple (index, image)
                 collisions=None,
                 # Les collisions sont représentées par une liste 2D composée de nombres (voir `mod/collisions.py`)
                 entities=None  # Les entities
                 ) -> None:
        # Afin d'éviter des problèmes liés aux références mémoires si nous utilisons
        # une list, nous prenons par défaut None et déclarons sur le tas
        if layers is None:
            layers = []
        if collisions is None:
            collisions = []
        if entities is None:
            entities = []
        self.map = map_background
        self.layers = layers
        self.layers.sort(key=lambda l: l[0])  # Cette ligne permet de trier les couches par leur index
        self.collisions = collisions
        self.entities = entities

    def draw(self, screen: pygame.Surface, camera: Camera, player: Player, zone_decals: Tuple[int, int], assets: Assets,
             map) -> None:
        # On calcule nos coordonnées selon la caméra et une variable `zone_decals` Voir `mod/camera.py` pour le
        # fonctionnement de la caméra Concernant `zone_decals`, cette variable a été implémentée à cause des soucis
        # embêtant quand la fenêtre est redimensionnée. En étant redimensionnée, la carte se déplaçait, mais pas le
        # joueur, ce qui était bien embêtant.
        coords = (
            camera.x + (zone_decals[0] // 2),
            camera.y + (zone_decals[1] // 2)
        )

        # Dessin de la carte en fond
        screen.blit(self.map, coords)

        # Cette variable permet de savoir si le joueur a été dessiné
        player_drawn = False

        # On prend l'index et l'image de chaque couche
        # Les couches sont déjà triées
        for i, layer in self.layers:
            # On regarde si le joueur n'a pas été dessiné et s'il est à cette couche
            if (not player_drawn) and player.layer == i:
                # Dans ce cas, on dessine le joueur et on déclare qu'il a été dessiné
                player.draw(screen, assets, camera, map)
                player_drawn = True
            # On dessine la couche
            screen.blit(layer, coords)

        # Si le joueur n'a pas été dessiné, on le dessine à la fin
        if not player_drawn:
            player.draw(screen, assets, camera, map)

        """
        [!] Le code ci-dessous est experimental
        
        #TODO
        """

        player_x = (screen.get_width() // 2)
        player_y = (screen.get_height() // 2)

        player.draw_remaining_defense(player_x, player_y, screen, (CASE_SIZE // 2))
        player.draw_remaining_life(player_x, player_y, screen, (CASE_SIZE // 2))

        player.draw_current_item(screen, assets)


class Map:
    """
    Cette class représente la carte
    
    La carte est composée de plusieurs zones, qu'on peut aussi voir comme des régions du monde.
    """

    def __init__(self) -> None:
        # On définit un attribut `zones` qui est un dictionnaire
        #   où les clés sont des valeurs de l'énumérateur `ZoneType` et la valeur est un objet de la class `Zone`
        self.zones: Dict[ZoneType, Zone] = {
            ZoneType.START: Zone(
                # On déclare le fond de cette zone
                pygame.image.load("assets/map/start_map_down2.png").convert_alpha(),
                # On déclare les couches
                [
                    (
                        0,
                        pygame.transform.scale(
                            pygame.image.load("assets/map/start_map_up2.png").convert_alpha(),
                            (2048 * 4, 2048 * 4)
                        )
                    )
                ],
                # Les collisions sont déclarées par la variable `START_COLLISIONS` (voir `mod/collisions.py`)
                collisions=START_COLLISIONS,
            )
        }

        # L'attribut `actual_zone` est de type `Zone', et est au départ la zone "START"
        self.actual_zone: Zone = self.zones[ZoneType.START]
        # Le fameux décalage de la fenêtre quand on la redimensionne
        self.zone_decals: Tuple[int, int] = (0, 0)
        self.DEFAULT_ZONE_DECALS = ()

    def draw(self, screen: pygame.Surface, assets: Assets, camera: Camera, player: Player) -> None:
        self.actual_zone.draw(screen, camera, player, self.zone_decals, assets, self)
