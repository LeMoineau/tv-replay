# IMPORT: LIB
from __future__ import unicode_literals
import youtube_dl


class Downloader:
    """
    Classe downloader pour télécharger des vidéos sur internet complétement porté par la library youtube_dl

    source: 
    - https://github.com/ytdl-org/youtube-dl/
    - https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py
    """

    def __init__(self):
        pass

    def download_video(self, url, format=None, filename=None, callback_progression=None):
        """
        Télécharge une vidéo à partir de son url

        parameters:
        - url: dict de la video à télécharger
        - format: (optionnel) dict du format choisis pour la video selectionnée
        - filename: (optionnel) nom du fichier vidéo en sortie 
        - callback_progression: (optionnel) function à appeler pour renvoier les informations de progression du téléchargement
        """
        if not format:
            format = self.extract_infos(url)

        ydl_opts = {
            "format": format["format_id"],  # ex: 'HLS_XQ_2-929'
            "progress_hooks": [
                callback_progression
            ] if callback_progression is not None else [],
        }

        if filename:
            ydl_opts["outtmpl"] = filename + "." + format["ext"]

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def get_formats(self, url):
        """
        Renvoie tous les formats disponibles pour une url de vidéo donnée

        parameters:
        - url: url de la video dont il faut récuperer les formats

        returns:
        - formats: liste des formats disponible pour la vidéo
        """
        opts = {
            "quiet": True
        }

        with youtube_dl.YoutubeDL(opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            formats = meta.get('formats', [meta])
        return formats

    @staticmethod
    def extract_infos(url):
        """
        Extrait toutes les infos que YoutubeDL possede pour l'url donne

        parameters:
        - url: url de la video de laquelle extraire les infos

        returns:
        - infos: [dict] des infos que possede YoutubeDL sur la video a l'url donne
        """
        ydl_opts = {
            "quiet": True,
            "simulate": True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            infos = ydl.extract_info(url)
        return infos


if __name__ == "__main__":
    dler = Downloader()
    # infos = dler.extract_infos("https://www.arte.tv/fr/videos/100748-001-A/toxic-tour-1-6/")
    # print(infos.keys())

    # preuve fonctionnemnt de yt-dl pour videos sur youtube: https://www.youtube.com/watch?v=9w_zn3uRwPU 
    yt_url = "https://www.youtube.com/watch?v=9w_zn3uRwPU"
    formats = dler.get_formats(yt_url)
    print("formats", formats)
    dler.download_video(yt_url)
