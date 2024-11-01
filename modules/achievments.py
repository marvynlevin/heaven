from enum import Enum
from typing import List

"""
Ce fichier contient le système de succès
"""


class AchievementsID(Enum):
    WALK_10000_STEPS = 0  # Marcher 10 000 pas
    FIRST_PARTY = 1  # Lancer une partie pour la première fois
    GET_THE_OLD_ADVENTURE = 2  # Charger une sauvegarde
    WATCH_CREDITS = 3  # Regarder les crédits


class Achievement:
    """
    Cette class représente un succès
    """

    def __init__(self, success_name: str, success_id: AchievementsID, description: str, completed: bool = False) -> None:
        self.name = success_name
        self.id = success_id
        self.description = description

        self.completed = completed

    def complete(self):
        self.completed = True

    def uncompleted(self):
        self.completed = False


class AchievementsBank:
    """
    Cette class contient le système de gestion des succès
    """

    def __init__(self) -> None:
        # On stocke un dictionnaire qui contiendra en clé des AchievementsID et en valeur Achievement
        self.success = {}

    def register_success(self, success_id: AchievementsID, new_success: Achievement, force: bool = False):
        """
        Enregistre un succès dans la base de donnée grâce à son identifiant
        N'effectue l'action que si le succès n'est pas enregistré ou que `force` est vrai
        """
        if not (success_id in self.success) or force:
            self.success[success_id] = new_success

    def complete(self, success_id: AchievementsID):
        """
        Complète un succès 
        """
        if success_id in self.success:
            self.success[success_id].complete()

    def uncompleted(self, success_id: AchievementsID):
        """
        Déclare un succès comme "à faire"
        """
        if success_id in self.success:
            self.success[success_id].uncompleted()

    def is_complete(self, success_id: AchievementsID) -> bool:
        """
        Renvoi une boolean qui permet de savoir si un succès est complété
        """
        return (success_id in self.success) and self.success[success_id].completed

    def format(self, per_page: int = 5) -> List[List[Achievement]]:
        """
        Renvoie une list en 2D pour l'affichage des succès
        Comme c'est un système de pages, nous allons mettre au maximum 5 succès par pages (personnalisable)
        """
        # Contiendra toutes les pages
        pages: List[List[Achievement]] = []
        # Contient les succès qui sont sur le point d'être placées dans `pages`
        temp = []
        # On parcourt chaque succès
        for s in self.success.values():
            # On ajoute le succès à `temp`
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


# On déclare la banque de succès afin de pouvoir y accéder depuis n'importe où
achievements: AchievementsBank = AchievementsBank()

ACHIEVEMENTS_INFO = {
    AchievementsID.FIRST_PARTY: ("Première partie", "Lancer une partie pour la première fois"),
    AchievementsID.GET_THE_OLD_ADVENTURE: ("Retour en territoire connue", "Charger une ancienne sauvegarde"),
    AchievementsID.WALK_10000_STEPS: ("Une petite promenade", "Marcher 10.000 pas"),
    AchievementsID.WATCH_CREDITS: ("Regarder les crédits", "La patience il faudra.")
}

# On enregistre chaque évènement
for achievement, id in AchievementsID.__members__.items():
    # On récupère le nom et la description
    name, desc = ACHIEVEMENTS_INFO[id]
    success = Achievement(name, id, desc, completed=False)
    achievements.register_success(id, success, force=False)
