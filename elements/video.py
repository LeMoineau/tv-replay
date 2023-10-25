# IMPORT: PROJECT
from elements.node import Node
from web.downloader import Downloader


class Video(Node):
    """
    Noeud d'une video pouvant etre telechargee

    parameters:
    - subtitle: sous-titre de la video
    - description: description de la video
    - duree: duree de la video
    - date: date de publication sur le site de la video
    - thumbail: image de la video
    - downloader: [Downloader] associe a la video pour la telecharger
    """
    
    def __init__(self, url, title=None, subtitle="", description="", duree=None, date=None,
                 thumbnail=None, children=[]):
        super().__init__(url, title, children)
        self.subtitle = subtitle
        self.description = description
        self.duree = duree
        self.date = date
        self.thumbnail = thumbnail
        self.downloader = Downloader()

    def extract_infos(self):
        """
        Retourne le dictionnaire des infos que YoutubeDL possede sur la video courante

        returns:
        - infos: [dict] contenant les infos que YoutubeDL a sur la video courante
        """
        return self.downloader.extract_infos(self.url)

    def get_formats(self):
        """
        Retourne la liste des formats que YoutubeDL a pour la video courante

        returns:
        - formats: [list] contenant tous les formats disponibles pour la video courante
        """
        return self.downloader.get_formats(self.url)

    def download(self, format=None, filename=None):
        """
        Telecharge la video courante au format choisi et sous le nom donne

        parameters:
        - format: (optionnel) format choisi pour le telechargement de la video
        - filename: (optionnel) nom a donne a la video en sortie
        """
        self.downloader.download_video(self.url, format, filename)

    def __str__(self):
        urlStr = f' url="{self.url}",' if isinstance(self.url, str) else ""
        res = f"---<video:{urlStr} " \
              f"title='{self.title}', " \
              f"subtitle='{self.subtitle}', " \
              f"description='{self.description}', " \
              f"duree='{self.duree}', date='{self.date}', " \
              f"thumbnail='{self.thumbnail}', " \
              f"len_children={len(self.children)}>"

        # for c in self.children:
        #     res += f"\n{str(c)}" # peut faire des boucles infini
        return res
