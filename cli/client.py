
# IMPORT: SYSTEM LIB
import os
import sys

# IMPORT: LIB
import datetime
from datetime import datetime

from colorama import Fore, Style

# IMPORT: PROJECT
from cli.parser import Parser
from cli.printer import Printer
from elements.channels.artetv import ArteTV
from cli import utils
from enums import enum_site

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Client:
    """
    Classe gerant toutes les manipulations sur la version terminal du programme Replay TV

    attributes:
    - _parser: [Parser] associe au [Client] courant
    - _printer: [Printer] associer au [Client] courant
    - current_node_selected: [Node] actuellement selectionnee
    - prompt: [list] representant le chemin d'acces au noeud [current_node_selected]
    """
    
    def __init__(self, parser):
        self._parser = parser
        self._printer = Printer()

        self.current_node_selected = None
        self.prompt = []

    def run(self):
        """
        Lance le client terminal du programme Replay TV
        """
        self._printer.print_title()
        self._printer.print_help()

        site_arg = self._parser.get_arg("site")
        if not site_arg:
            site_arg = self._selection_site()
            print("")

        self.prompt.append(site_arg)

        self._printer.print_message(f"Site source selectionné: {site_arg}", site_arg)
        self.site_class = enum_site[site_arg]["crawler"]()
        self._printer.print_message(f"Choix du crawler {self.site_class.crawler.driverName}",
                                    self.site_class.crawler.driverName)
        self._printer.print_message(f"Lancement du crawler {site_arg}...", site_arg)
        self.site_class.init()

        self.current_node_selected = self.site_class

        cmd = "cd"
        while cmd != "exit":
            current_table = self._printer.print_table_node(self.current_node_selected,
                                                           showTable=False)
            cmd = self._printer.print_input("\nQue voulez-vous faire ?", "/".join(self.prompt))
            self.process_cmd(cmd, current_table)

        self.site_class.dispose()

    def _selection_site(self):
        """
        Demande a l'utilisateur de selectionner un site parmi les sites disponibles (cf enums.enum_site)

        returns:
        - input: le nom du site selectionne par l'utilisateur
        """
        list_site = {"arte": ArteTV}
        self._printer.print_message("Liste des sites disponibles:")
        for s, v in enum_site.items():
            self._printer.print_message(f" - {s}: {v['description']}", s)
        return self._printer.print_input("\nDe quel site voulez-vous prendre les videos ?", "site",
                                         lambda x: x not in list_site.keys(),
                                         "ce site n'est pas dans la liste des sites disponibles")

    def process_cmd(self, cmd, current_table):
        """
        Lance la fonction de la commande entre par l'utilisateur

        parameter:
        - cmd: [str] de la commande demandee
        - current_table: [dict] des enfants du noeud [current_node_selected] actuellement selectionne
        """
        args = cmd.split(" ")
        if args[0] == "cd":
            self.cd(args[1:], current_table)
        elif args[0] == "help":
            self.help()
        elif args[0] == "info":
            self.info(args[1:], current_table)
        elif args[0] == "search":
            self.search(args[1:])
        elif args[0] == "dl":
            self.dl(args[1:], current_table)
        elif args[0] == "guide":
            self.guide(args[1:])
        elif args[0] == "ls":
            self.ls()
        elif args[0] != "exit":
            self._printer.print_error(f'aucune commande trouvée pour "{cmd}"')
            self._printer.print_help()

    def cd(self, args, current_table):
        """
        Deplace l'utilisateur de noeud

        parameters:
        - args: [list] des arguments apres 'cd'. Seul le premier element sera utilise pour dirigier l'utilisateur
        - current_table: [dict] des enfants du noeud [current_node_selected] actuellement selectionne
        """
        if len(args) >= 1:
            index = args[0]
            if index in current_table.keys():
                self.current_node_selected = current_table[index]
                if index == "..":
                    self.prompt.pop()
                else:
                    self.prompt.append(self.current_node_selected.title)
                if utils.get_node_type(self.current_node_selected) != "Channel" and len(
                        self.current_node_selected.children) <= 0:
                    if self.current_node_selected.url == self.site_class.guide_tv:
                        self.guide(args[1:], from_node=self.current_node_selected)
                    else:
                        getattr(self.site_class,
                                f"crawl_{utils.get_node_type(self.current_node_selected).lower()}")(
                            self.current_node_selected)
            else:
                self._printer.print_error(f"argument invalide, l'id '{index}' n'existe pas")
        else:
            self._printer.print_error(f"commande incorrect, il manque 1 parametre")
            self._printer.print_warning(
                f"{Fore.MAGENTA}usage {Style.BRIGHT}cd <id_noeud> {Style.RESET_ALL}")

    def ls(self):
        """
        Affiche la liste des enfants du noeud actuellement selectionne ([current_node_selected])
        """
        self._printer.print_table_node(self.current_node_selected)

    def guide(self, args, from_node=None):
        """
        Ajoute une categorie correpondant a la date selectionne dans [args] dans le noeud [from_node]

        parameters:
        - args: [list] des arguments apres 'guide'. Seul le premier argument sera lu et devrai etre au format jj/mm/AA (exemple: 05/07/2001)
        - from_node: (optionnel) [Node] dans lequel ajouter la nouvel categorie, sinon la racine de la chaine 
        """
        date = datetime.date.today()
        current_path = from_node.get_path() + "/" + from_node.title if from_node else self.site_class.title
        if len(args) >= 1:
            try:
                date = datetime.datetime.strptime(args[0], '%d/%m/%Y')
            except Exception:
                self._printer.print_error(
                    f"la date {args[0]} entree n'est pas valide, veuillez entrer une date au "
                    f"format dd/MM/yyyy (ex: 05/07/2001)")
                return
        self._printer.print_message(f"Crawling du Guide TV du {date.strftime('%d/%m/%Y')}...",
                                    to_highlight=f"{date.strftime('%d/%m/%Y')}")
        self.site_class.crawl_guide_tv(date=date, from_node=from_node)
        self._printer.print_message(f"Noeud du Guide TV créé à la racine {current_path}/",
                                    to_highlight=f"{current_path}/")

    def info(self, args, current_table):
        """
        Affiche la liste des infos du noeud selectionne

        parameters:
        - args: [list] des arguments apres 'info'. Seul le premier argument sera lu pour selectionne la video de laquelle recuperer les infos
        - current_table: [dict] des enfants du noeud [current_node_selected] actuellement selectionne
        """
        if len(args) >= 1:
            index = args[0]
            if index in current_table.keys():
                current_node = current_table[index]
                node_infos = vars(current_node)
                print("\n[Informations de ArteTV]")
                self._printer.print_node_infos(node_infos)
                self._printer.print_message(f"type: {utils.get_node_type(current_node)}", "type")
                if utils.get_node_type(current_node) == "Video":
                    ytdl_infos = current_node.extract_infos()
                    self._printer.print_message(f"\n[Informations de YoutubeDL]")
                    self._printer.print_node_infos(ytdl_infos)
            else:
                self._printer.print_error(f"argument invalide, l'id '{index}' n'existe pas")
        else:
            self._printer.print_error(f"commande incorrect, il manque 1 paramètre")
            self._printer.print_warning(
                f"{Fore.MAGENTA}usage {Style.BRIGHT}info <id_noeud> {Style.RESET_ALL}")

    def search(self, args):
        if len(args) >= 1:
            self.site_class.crawl_research(args)
            self._printer.print_message(
                f"Noeud de la recherche créé à la racine {self.site_class.title}/",
                to_highlight=f"{self.site_class.title}/")
        else:
            self._printer.print_error(f"votre recherche doit contenir au moins 1 mot")

    def dl(self, args, current_table):
        """
        Telecharge une video selectionnee

        parameters:
        - args: [list] des arguments apres 'dl'. Seul le premier argument sera lu pour selectionne la video a telecharger
        - current_table: [dict] des enfants du noeud [current_node_selected] actuellement selectionne
        """
        if len(args) >= 1:
            index = args[0]
            if int(index) in current_table.keys():
                current_node = current_table[int(index)]
                if utils.get_node_type(current_node) == "Video":
                    # Choix nom fichier
                    rep = self._printer.print_input(
                        "\nVoulez-vous sauvegarder la vidéo sous un nom particulier ? (Y/n)", "#")
                    if rep == "Y":
                        filename = self._printer.print_input(
                            "\nSous quel nom voulez-vous sauvegarder la vidéo ?", "filename")
                    else:
                        filename = None
                    # Choix format vidéo
                    rep = self._printer.print_input(
                        "\nVoulez-vous choisir un format particulier pour la vidéo ? (Y/n)", "#")
                    if rep == "Y":
                        formats = current_node.get_formats()
                        id_format = "-1"
                        while int(id_format) < 0 or int(id_format) >= len(formats):
                            self._printer.print_regular_table(formats,
                                                              ["format_id", "format", "ext"],
                                                              "Liste des formats disponibles pour la vidéo")
                            id_format = int(
                                self._printer.print_input("\nQuel format voulez-vous choisir ?",
                                                          "id"))
                            id_format -= 1
                            if int(id_format) < 0 or int(id_format) >= len(formats):
                                self._printer.print_error(
                                    f"le format #{id_format + 1} n'existe pas, veuillez en choisir un autre")
                            else:
                                self._printer.print_message(
                                    f"format selectionné: {formats[int(id_format)]['format']}",
                                    formats[int(id_format)]['format'])
                        form = formats[int(id_format)]
                    else:
                        form = None
                    # Telechargement de la video
                    current_node.download(form, filename)
                else:
                    self._printer.print_error(
                        f"argument invalide, le noeud #{index} selectionné n'est pas une vidéo")
            else:
                self._printer.print_error(f"argument invalide, l'id '{index}' n'existe pas")
        else:
            self._printer.print_error(f"commande incorrect, il manque 1 paramètre")
            self._printer.print_warning(
                f"{Fore.MAGENTA}usage {Style.BRIGHT}info <id_noeud> {Style.RESET_ALL}")

    def help(self):
        """
        Affiche les aides du client terminal de Replay TV
        """
        self._printer.print_help()


if __name__ == "__main__":
    parser = Parser()
    parser.init()

    client = Client(parser)
    client.run()
