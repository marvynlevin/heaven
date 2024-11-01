from typing import Dict
import pygame
from enum import Enum

from constants import SOUND_CONFIG

"""

Ce module permet de gérer le système de musique dans le jeu

"""


class SoundsId(Enum):
    """
    Cet énumérateur déclare les différents identifiants de sons possibles
    """
    TEST = 0
    CRN_FTP_1 = 1  # Crunchy footsteps 1
    CRN_FTP_2 = 2  # Crunchy footsteps 2
    CRN_FTP_3 = 3  # Crunchy footsteps 3
    CRN_FTP_4 = 4  # Crunchy footsteps 4
    CRN_FTP_5 = 5  # Crunchy footsteps 5
    CRN_FTP_6 = 6  # Crunchy footsteps 6
    CRN_FTP_7 = 7  # Crunchy footsteps 7


# On déclare quels sons appartiennent à quelle catégorie
MUSIC_SOUNDS = [SoundsId.TEST]
PLAYER_SOUNDS = []
EFFECTS_SOUNDS = [
    SoundsId.CRN_FTP_1, SoundsId.CRN_FTP_2, SoundsId.CRN_FTP_3, SoundsId.CRN_FTP_4,
    SoundsId.CRN_FTP_5, SoundsId.CRN_FTP_6, SoundsId.CRN_FTP_7
]


def get_ctg_from_id(id: SoundsId) -> str:
    """
    Cette fonction permet de connaitre la catégorie de la musique
    """
    if id in MUSIC_SOUNDS:
        return "music"
    elif id in PLAYER_SOUNDS:
        return "player"
    else:
        return "global"


def calc_sound_volume(id: SoundsId) -> float:
    """
    Cette fonction renvoi le volume d'un son à partir des paramètres
    """
    ctg = get_ctg_from_id(id)
    if ctg == "global":
        return SOUND_CONFIG["global"] / 100
    return (SOUND_CONFIG["global"] / 100) * (SOUND_CONFIG[ctg] / 100)


class SoundsBank:
    """
    Cette class contient chaque son qui a été enregistré
    """

    def __init__(self) -> None:
        # Les sons seront stockés dans l'attribut "sounds" qui est un dictionnaire
        # où la clé est de type `SoundsId` et la valeur est le son pygame
        self.sounds = {}

    def load(self, sound_id: SoundsId, path: str):
        """
        Charge la musique
        Ne charge pas cette dernière si l'identifiant est déjà dans la base de donnée
        """
        assert type(sound_id) == SoundsId, "L'identifiant du son n'est pas valide"
        assert type(path) == str, "le chemin vers le son n'est pas un string"
        if not (sound_id in self.sounds):
            self.sounds[sound_id] = pygame.mixer.Sound(file=path)

    def get(self, id: SoundsId) -> pygame.mixer.Sound:
        """
        Renvoi la musique si elle a été chargée avec cet identifiant
        [!] Renvoi `None` si aucune musique ne possède cet identifiant n'est pas chargée
        """
        assert type(id) == SoundsId, "`id` doit être une variable de type `SoundsId`"
        if id in self.sounds:
            return self.sounds[id]


class Sound:
    """
    Cette class contrôle le système de musique
    
    Elle permet de controller les sons en train de jouer ou bien de jouer un son
    """

    def __init__(self) -> None:
        # On charge la banque de donnée des sons
        self.sounds_bank = SoundsBank()
        # On définit l'attribut `sounds_playings` qui permettra de savoir quels sons sont en train de jouer
        # Le dictionnaire possède en clés un `SoundsId` et une valeur qui est le canal audio sur lequel joue le son
        self.sounds_playings: Dict[SoundsId, pygame.mixer.Channel] = {}

    def load_sound(self, sound_id: SoundsId, path: str):
        """
        Charge la musique
        Ne charge pas cette dernière si l'identifiant est déjà dans la base de donnée
        """
        self.sounds_bank.load(sound_id, path)

    def play_sound(
            self,
            id: SoundsId,
            loops: int = 0,
            maxtime: int = 0,
            fade_ms: int = 0,
            force_playing: bool = False,
            volume: float = 101.0  # Le son ne sera donc pas changé dans ce cas, car il doit être inférieur à 100.
    ) -> bool:
        """
        Joue un son en l'identifiant avec son ID
        
        Renvoi un boolean ; True si le son joue, False sinon
        
        Prend en argument :
        - id : l'identifiant du son
        - loops : le nombre de répétitions
        - maxtime : le temps maximal pendant lequel le son peut jouer
        - fade_ms : le temps pendant lequel l'effet de "fade" joue (voir ci-dessous)
        - force_playing: joue la musique même si le son est en train d'être joué
        
        * `fade_ms`: (documentation de pygame)
        The fade_ms argument will make the sound start playing at 0 volume and fade up
        to full volume over the time given. The sample may end before the fade-in is complete.
        """
        # Si on ne doit pas jouer de son, on arrête maintenant
        if not SOUND_CONFIG["play"]:
            return False
        # On charge la musique
        sound = self.sounds_bank.get(id)
        # Si le son est None, c'est qu'il n'existe pas, alors on renvoie False
        # On renvoie également False si `force_playing` est False et que le son est déjà en train de jouer
        if (sound is None) or ((not force_playing) and (id in self.sounds_playings)):
            return False

        # On joue le son
        play_action = sound.play(loops, maxtime, fade_ms)
        self.sounds_playings[id] = play_action
        if 0.0 <= volume <= 100.0:
            self.change_volume(id, volume)
        # On renvoie True pour préciser que c'est un succès
        return True

    def stop_sound(self, id: SoundsId) -> bool:
        """
        Tente de stopper un son s'il est en cours de lecture
        """
        # On vérifie si le son joue
        # Pas besoin de vérifier qu'il existe, car le contenu de
        # `sounds_playings` est sûre
        if not (id in self.sounds_playings):
            return False

        # On récupère le son
        sound = self.sounds_bank.get(id)

        # On stop le son
        sound.stop()

        # On arrête également le channel et on le supprime des sons en cours de lecture
        self.sounds_playings[id].stop()
        del self.sounds_playings[id]

        return True

    def change_volume(self, id: SoundsId, volume: float) -> bool:
        """
        Change le volume d'un son en cours de lecture
        """
        assert (type(volume) in [float, int]) and (
                0.0 <= volume <= 100.0), "Le volume doit être un nombre flottant ou entier compris entre 0 et 100"

        # On vérifie si le son joue
        # Pas besoin de vérifier qu'il existe, car le contenu de
        # `sounds_playings` est sûre
        if not (id in self.sounds_playings):
            return False

        # On récupère le son
        sound = self.sounds_bank.get(id)

        # On change le volume
        sound.set_volume(volume / 100.0)
        return True

    def pause(self, id: SoundsId) -> bool:
        """
        Met en pause un son en cours de lecture
        """
        # On vérifie si le son joue
        # Pas besoin de vérifier qu'il existe, car le contenu de
        # `sounds_playings` est sûre
        if not (id in self.sounds_playings):
            return False

        # On récupère le canal audio sur lequel joue le son
        sound = self.sounds_playings[id]
        # On met en pause le son
        sound.pause()
        return True

    def resume(self, sound_id: SoundsId) -> bool:
        """
        Relance la lecture d'un son qui était en pause
        """
        # Si on ne doit pas jouer de son, on arrête maintenant
        if not SOUND_CONFIG["play"]:
            return False
        # On vérifie si le son joue
        # Pas besoin de vérifier qu'il existe, car le contenu de
        # `sounds_playings` est sûre
        if not (sound_id in self.sounds_playings):
            return False

        # On récupère le canal audio sur lequel est le son
        sound = self.sounds_playings[sound_id]
        # On re-joue le son
        sound.play()
        return True

    def pause_all_sounds(self):
        """
        Met en pause TOUS les sons en cours de lecture
        """
        for sound in self.sounds_playings.values():
            sound.pause()

    def resume_all_sounds(self):
        """
        Relance la lecture de TOUS les sons
        """
        for sound in self.sounds_playings.values():
            sound.unpause()

    def update_volumes(self):
        """
        Met à jour les volumes de chaque son selon les paramètres
        """
        for id, sound in self.sounds_playings.items():
            print("update volume for", id)
            vol = calc_sound_volume(id)
            if sound.get_volume() != vol:
                sound.set_volume(vol)

    def stop_sounds(self):
        """
        Coupe tous les sons
        """
        for id, sound in self.sounds_playings.items():
            sound.stop()

        self.sounds_playings = {}
