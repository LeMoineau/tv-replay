# IMPORT: LIB
import hashlib


class Node:
    """
    Classe principale representant chaque element et redirection importante d'un site

    attributes:
    - url: [str] de l'url correspondant au noeud courant
    - id: [str] de l'hashcode associer a l'url du noeud courant
    - title: [str] decrivant le noeud
    - children: [list] des noeuds contenu par le noeud courant
    - parent: [Node] noeud parent ou None si racine
    """
    
    def __init__(self, url, title=None, children=[]):
        self.url = url
        self.id = hashlib.sha256(str(self.url).strip().encode()).hexdigest()
        self.title = title if title else f"Node #{self.id}"
        self.children = children
        self.parent = None

    def add_child(self, child):
        """
        Ajoute un enfant au noeud courant

        parameters:
        - child: [Node] a ajouter au noeud courant
        """
        self.children.append(child)
        child.parent = self

    def get_child(self, url=None, id=None):
        """
        Retourne la liste des enfants ou le seul enfant par rapport aux parametres choisi

        parameters:
        - url: url que l'enfant doit avoir
        - id: id que l'enfant doit avoir

        returns:
        - res: liste des enfants ou enfant seul correspond aux elements de recherche 
        """
        for c in self.children:
            if (url and c.url == url) or (id and c.id == id):
                return c
            recursif_node = c.get_child(url=url, id=id)
            if (isinstance(recursif_node, list) and len(recursif_node) > 0) or isinstance(
                    recursif_node, Node):
                return recursif_node
        return []

    def get_path(self):
        """
        Retourne un [str] representant le chemin d'acces au noeud actuel

        returns:
        - res: [str] representant le chemin d'acces au noeud actuel de la forme '<title1>/<title2>'
        """
        p = self.parent
        res = list()
        while p is not None:
            res.append(p.title)
            p = p.parent
        return '/'.join(res)

    def get_type_str(self):
        """
        Retourne le nom de la classe etendu du noeud actuel ('Categorie', 'Section', ...)

        returns:
        - type: [str] du nom de la classe etendu du noeud actuel
        """
        return type(self).__name__

    def __str__(self):
        res = f"<node: url='{self.url}', len_children={len(self.children)}>"
        for c in self.children:
            res += f"\n{str(c)}"
        return res


if __name__ == "__main__":
    n = Node("arte.tv/fr")
    print(n.id)
    n2 = Node("google.com")
    print(n2.id)
    n3 = Node("arte.tv/fr")
    print(n3.id)
