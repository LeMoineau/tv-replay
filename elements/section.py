# IMPORT: PROJECT
from elements.node import Node


class Section(Node):
    """
    Noeud particulier representant une sous partie d'une categorie d'un site et contenant des videos

    attributes:
    - html_element: element HTML associe a la section
    - description: [str] decrivant la section
    """
    
    def __init__(self, url, title, html_element, description=""):
        super().__init__(url, title, [])
        self.html_element = html_element
        self.description = description

    def __str__(self):
        res = f"--<section #{self.id}: " \
              f"title='{self.title}', " \
              f"description='{self.description}', " \
              f"len_children={len(self.children)}>"

        for c in self.children:
            res += f"\n{str(c)}"
        return res
