from entities.parent import Entity, EntityType
from modules.assets import Assets
from modules.camera import Camera
from constants import *

"""

[!] Code experimental

Non documenté & Optimisé car le système d'entités n'est pas implémenté

"""


class Spirit(Entity):
    def __init__(self, x=0, y=0) -> None:
        super().__init__((x, y), 5, EntityType.SPIRIT, "test_spirit")

    def update(self, frequence: pygame.time.Clock, delta: float):
        pass

    def draw(self, screen: pygame.Surface, assets: Assets, camera: Camera):
        player_surface = assets.get(self.asset)
        if not (player_surface is None):
            screen.blit(
                player_surface,
                (
                    self.x + (screen.get_width() // 2) - (CASE_SIZE // 2) + camera.x,
                    self.y + (screen.get_height() // 2) - (CASE_SIZE // 2) + camera.y
                )
            )
