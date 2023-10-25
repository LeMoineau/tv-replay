class EmptyElement:
    """
    Element de recherche vide contenant juste un [text] vide
    """
    def __init__(self):
        self.text = ""

    def get_attribute(self, name=None):
        """
        Fonction d'imitation de [get_attribute] sur les elements HTML de selenium

        parameters:
        - name: imitation du parametre de la fonction [get_attribute] des elements HTML de selenium

        returns:
        - res: [str] vide
        """
        return ""
