from enum import Enum


class ItemType(Enum):
    """
    Enumère les différents items possibles
    """
    WOOD = 0
    WOOD_SWORD = 1

    def __repr__(self) -> str:
        return str(self)


class Item:
    """
    Cette class permet de définir un objet (item) avec une quantité, un asset (icon) et un type
    """

    def __init__(self, asset: str, item_type: ItemType, quantity: int = 1) -> None:
        self.quantity = quantity
        self.asset = asset
        self.type = item_type

    def edit_stocks(self, n: int) -> bool:
        """
        Ajoute ou retire une partie du stock
        """
        if self.quantity + n < 0:
            return False
        else:
            self.quantity += n
            return True

    def __repr__(self) -> str:
        return f"[{self.type}; {self.asset}]({self.quantity})"


class Wood(Item):
    """
    Class pour l'item de bûche de bois
    """

    def __init__(self, quantity: int = 1) -> None:
        super().__init__("item_wood", ItemType.WOOD, quantity)


class WoodSword(Item):
    """
    Class pour l'item d'épée faite de bois
    """

    def __init__(self, damage=10, durability=100) -> None:
        super().__init__("item_wood_sword", ItemType.WOOD_SWORD, 1)

        self.damage = damage
        self.durability = durability


class Inventory:
    """
    Cette class représente l'inventaire du joueur
    """

    def __init__(self) -> None:
        # l'attribut `item` est un dictionnaire vide au départ
        self.items = {}

    def add_item(self, item: Item, force=False) -> bool:
        """
        Ajoute un item à partir d'un argument `item` de type `Item`
            et un attribut secondaire `force` pour forcer le remplacement
        
        Si force est `False`, alors l'item ne sera ajouté que s'il n'est pas présent.
        
        Renvoi une boolean correspondant au succès (ou non) de l'opération
        """
        if not (item.type in self.items.keys()) or force:
            self.items[item.type] = item
            return True
        return False

    def remove_item(self, item_type: ItemType):
        """
        Retire un item de l'inventaire
        """
        if item_type in self.items.keys():
            del self.items[item_type]

    def __repr__(self) -> str:
        return str(self.items)
