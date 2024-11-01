import datetime
import json
from typing import Dict, List, Tuple

from modules.map import Map
from constants import *


def load_save() -> Map:
    """
    Renvoi la carte à partir d'une sauvegarde
    Non implémentée
    """
    map = Map()
    return map


def init_save_system():
    """
    Cette fonction crée le dossier à l'addresse `SAVE_DIR` s'il n'existe pas
    """
    if not os.path.isdir(SAVE_DIR):
        os.mkdir(SAVE_DIR)


class GameSave:
    """
    Cette class représente la sauvegarde d'une partie
    """

    def __init__(self, raw: Dict, id: int, path: str, opened: bool = False):
        self.open = opened

        # On récupère la date de la dernière modification
        # La date est en tant UNIX basé sur l'heure UTC+0
        if "date" in raw:
            # Nous avons déjà un temp sauvegardé

            if type(raw["date"]) == datetime.datetime:
                self.date = raw["date"]
            else:
                self.date = datetime.datetime.fromtimestamp(raw["date"])
        else:
            # On prend la date actuelle :)
            self.date = datetime.datetime.now(tz=datetime.timezone.utc)

        # On récupère la date de création
        # La date est en tant UNIX basé sur l'heure UTC+0
        if "created_at" in raw:
            # Nous avons déjà un temp sauvegardé

            if type(raw["created_at"]) == datetime.datetime:
                self.created_at = raw["created_at"]
            else:
                self.created_at = datetime.datetime.fromtimestamp(raw["created_at"])
        else:
            # On prend la date actuelle :)
            self.created_at = datetime.datetime.now(tz=datetime.timezone.utc)

        # On stocke l'identifiant
        self.id = id

        # On stocke le chemin à lequel est la sauvegarde
        self.path = path

        # On récupère les coordonnées du joueur
        if ("player_coords" in raw) and (type(raw["player_coords"]) == list) and (len(raw["player_coords"]) == 2) and (
                (type(raw["player_coords"][0]) in [float, int]) and (type(raw["player_coords"][1]) in [float, int])):
            # Les coordonnées sont correctes, on ajoute ca :)
            self.player_coords = raw["player_coords"]
        else:
            # Sinon, on met les coordonnées de base
            self.player_coords = PLAYER_START_COORDS

    def __eq__(self, v) -> bool:
        """
        Cette fonction permet de vérifier si deux sauvegardes sont identiques
        """
        return self.player_coords == v.player_coords

    def __repr__(self) -> str:
        return "GameSave" + f"[{self.id}]" + "{ player_coords: " + str(self.player_coords) + ", date: " + str(
            self.date) + "}"

    def save(self, game):
        """
        Cette fonction permet de sauvegarder la partie
        """

        # On prépare le terrain pour transformer les données au format JSON
        save = {
            "created_at": self.date.timestamp(),
            "date": datetime.datetime.now().timestamp(),
            "player_coords": [game.player.x, game.player.y]
        }

        # On écrit sur le fichier
        with open(self.path, 'w', encoding="utf8") as f:
            f.write(json.dumps(save))
            f.close()

        print(f"save {self.id} saved")


def read_dir(path: str, wanted_extension: str) -> List[Tuple[str, str]]:
    """
    Cette fonction renvoie tous les fichiers d'une extension souhaitée
    en regardant dans les dossiers et sous-dossiers.
    Si nous prenons, par exemple, les extensions JSON, alors `wanted_extension` doit être ".json"
    """
    files = []
    for (dirpath, __dirnames, filenames) in os.walk(path):
        files.extend([
            (os.path.join(dirpath, f), f.replace(wanted_extension, ""))
            for f in filenames if f.endswith(wanted_extension)
        ])
    return files


class SaveBank:
    """
    Cette class contient toutes les sauvegardes
    """

    def __init__(self) -> None:
        self.saves = {}

        self.update()

    def update(self):
        """
        Met à jour les sauvegardes
        """
        saves_query = read_dir(SAVE_DIR, ".json")

        saved_id = []

        for save_path, save_id in saves_query:
            # On vérifie que c'est bien un fichier et qu'il termine par ".json"
            if os.path.isfile(save_path) and save_path.endswith(".json"):
                # On lis le fichier
                with open(save_path, "r", encoding="utf8") as f:
                    save_data = json.load(f)
                    f.close()

                # On vérifie que le type est un dictionnaire
                if type(save_data) == dict:
                    # Si oui, ont créé la sauvegarde
                    save = GameSave(save_data, int(save_id), save_path)

                    # Et on vérifie que, soit, la sauvegarde n'est pas encore enregistrée, soit elle est différente
                    if not (int(save_id) in self.saves) or (save != self.saves[int(save_id)]):
                        self.saves[int(save_id)] = save
                        saved_id.append(int(save_id))

        # On supprime les sauvegardes qui n'existent plus
        for save_id in list(self.saves.keys()):
            if not (save_id in saved_id):
                del self.saves[save_id]

    def save(self, id: int, game) -> bool:
        """
        Enregistre sur le disque dur une sauvegarde qui est en mémoire
        Renvoie False si l'id n'existe pas
        """
        print("saving ", id, "...")

        print(self.saves)

        if not (id in self.saves):
            return False

        print("save", id)

        self.saves[id].save(game)

    def format(self, per_page: int = 5) -> List[List[GameSave]]:
        """
        Renvoie une list en 2D pour l'affichage des sauvegardes
        Comme c'est un système de pages, nous allons mettre au maximum 5 sauvegardes par pages (personnalisable)
        """
        # Contiendra toutes les pages
        pages = []
        # Contient les sauvegardes qui sont sur le point d'être placées dans `pages`
        temp = []
        # On parcourt chaque sauvegarde
        for s in sorted(self.saves.values(), key=lambda sv: sv.id):
            # On ajoute la sauvegarde à `temp`
            print(s.id, "=", s.open)
            # TODO: Quand on n'a que deux sauvegardes, elles alternent entre ouvertes et fermées (une seule à la fois wtffff)
            if not s.open:
                temp.append(s)
            # Si `temp` a atteint ou dépassé la longueur par page demandée,
            # alors on ajoute `temp` aux pages et on nettoie `temp`
            if len(temp) >= per_page:
                pages.append(temp)
                temp = []
        # On vérifie une dernière fois pour éviter toute oublie
        if len(temp) > 0:
            pages.append(temp)
        return pages


saves: SaveBank = SaveBank()


def save_configuration():
    """
    Sauvegarde la configuration actuelle
    """
    config = {
        "key_bindings": KEYS_BINDINGS,
        "sound": SOUND_CONFIG
    }

    # On transforme le dictionnaire `config` en string
    jsoned_config = json.dumps(config)

    with open("./config.json", "w", encoding="utf8") as f:
        # On écrit la configuration puis on quitte
        f.write(jsoned_config)
        f.close()


def load_config():
    """
    Charge la configuration qui était sauvegardée
    """
    with open("./config.json", "r", encoding="utf8") as f:
        config = json.load(f)

    if type(config) != dict:
        # La configuration est corrompue
        # On va alors tout réinitialiser
        os.remove("./config.json")
        # On ne va pas plus loin, la configuration est déjà par défaut
        return

    # On regarde si il y a la clé "key_bindings"
    if "key_bindings" in config and (type(config["key_bindings"]) == dict):
        # On vérifie chaque entrée pour être sûr :
        for k in KEYS_BINDINGS.keys():
            if k in config["key_bindings"] and (type(config["key_bindings"][k]) == int):
                KEYS_BINDINGS[k] = config["key_bindings"][k]

    # On regarde si il y a la clé "sound"
    if "sound" in config and (type(config["sound"]) == dict):
        # On va prendre chaque paire de clé-valeur et vérifier
        for k in SOUND_CONFIG.keys():
            if k in config["sound"] and (type(config["sound"][k]) == type(SOUND_CONFIG[k])):
                SOUND_CONFIG[k] = config["sound"][k]
