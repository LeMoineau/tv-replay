# IMPORT: PROJECT
from elements.node import Node


class Categorie(Node):
    """
    Une categorie est un noeud représentant un sous-ensemble d'une page.

    Par exemple, le site ArteTV contient les catégories:
    - Accueil
    - Emissions
    - ...etc
    """

    def __init__(self, url, title=None, infos={}):
        super().__init__(url, title, [])
        self.infos = infos

    def get_child(self, url=None, title=None, id=None):
        """
        Retourne la liste des enfants ou le seul enfant par rapport aux parametres choisi

        parameters:
        - url: url que l'enfant doit avoir
        - title: title que l'enfant doit avoir
        - id: id que l'enfant doit avoir

        returns:
        - res: liste des enfants ou enfant seul correspond aux elements de recherche 
        """
        if title:
            res = [c for c in self.children if c.title == title]
            return res[0] if len(res) == 1 else res
        else:
            return super().get_child(url=url, id=id)

    def __str__(self):
        res = f"-<categorie: " \
              f"url='{self.url}', " \
              f"title='{self.title}', " \
              f"len_children={len(self.children)}>"

        for c in self.children:
            res += f"\n{str(c)}"
        return res
