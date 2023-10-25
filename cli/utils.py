# IMPORT: PROJECT
from elements.channel import Channel


def get_node_type(node):
    """
    Renvoie le [str] du nom de la classe du noeud [node]
    
    parameters:
    - node: [Node] duquel prendre le nom de classe

    returns:
    - type: [str] du nom de la classe de [node] et 'Channel' si une classe particuliere (exemple: ArteTV -> Channel)
    """
    return type(node).__name__ if not isinstance(node, Channel) else "Channel"
