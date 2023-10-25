# IMPORT: SYSTEM LIB
import os
import sys

# IMPORT: LIB
from colorama import Fore, Style
from tabulate import tabulate

# IMPORT: PROJECT
from elements.video import Video
from cli import utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Printer:
    """
    Classe regroupant toutes les methodes d'affichage dans le terminal dans un souci d'uniformisation
    """
    
    def __init__(self):
        self.CMD_COLOR = Fore.MAGENTA
        self.CMD_STYLE_1 = Fore.CYAN
        self.CMD_STYLE_2 = Fore.BLUE
        self.CMD_WARNING = Fore.YELLOW
        self.CMD_ERROR = Fore.RED
        self.CMD_STANDARD = Fore.WHITE
        self.CMD_HIGHLIGHT = Fore.CYAN

    def print_title(self):
        """
        Affiche le title du client terminal 'TV-Replay Client'
        """
        print(f"{self.CMD_STYLE_2}+{self.CMD_STYLE_1}---------------------------{self.CMD_STYLE_2}+")
        print(f"{self.CMD_STYLE_1}|                           |")
        print(f"{self.CMD_STYLE_1}|{Fore.WHITE}      TV-Replay Client     {self.CMD_STYLE_1}|")
        print(f"{self.CMD_STYLE_1}|                           |")
        print(f"{self.CMD_STYLE_2}+{self.CMD_STYLE_1}---------------------------{self.CMD_STYLE_2}+{Style.RESET_ALL}")

    def print_help(self):
        """
        Affiche les aides (commandes disponibles) dans le client terminal
        """
        print(f"\nCommandes utiles:")
        self.print_cmd("help", message="affiche l'aide")
        self.print_cmd("cd", "id_noeud", "naviguer dans l'arbre du site")
        self.print_cmd("guide", "date dd/MM/yyyy",
                       message="affiche le programme pour un jour donne")
        self.print_cmd("info", "id_noeud", "avoir les informations d'un noeud")
        self.print_cmd("search", "recherche", "faire une recherche sur le site")
        self.print_cmd("dl", "id_video", "telecharger une video")
        self.print_cmd("ls", message="affiche le repertoire courant")
        self.print_cmd("exit", message="sortir du programme")
        print("")

    def print_cmd(self, cmd, params=[], message=None):
        """
        Affiche un rappel d'une commande dans le terminal

        parameters:
        - cmd: [str] de la commande a afficher (exemple: ls, cd...)
        - params: [list] des parametres de la commande
        - message: [str] decrivant l'effet de la commande 
        """
        if not message:
            message = f"commande {cmd}"
        tmp = ""

        if isinstance(params, list):
            for p in params:
                tmp += f" <{p}>"
        elif isinstance(params, str):
            tmp = f" <{params}>"

        print(f" - {self.CMD_COLOR}{Style.BRIGHT}{cmd}{Style.NORMAL}{tmp}{Style.RESET_ALL}:"
              f" {message}")

    def print_warning(self, message):
        """
        Affiche un message d'avertissement

        paramters:
        - message: message d'avertissement
        """
        print(f"{self.CMD_WARNING}Warning: {message}{Style.RESET_ALL}")

    def print_error(self, message):
        """
        Affiche un message d'erreur

        paramters:
        - message: message d'erreur
        """
        print(f"{self.CMD_ERROR}Error: {message}{Style.RESET_ALL}")

    def print_message(self, message, to_highlight=None):
        """
        Affiche un message en surlignant eventuellement certains passages

        parameters:
        - message: message a ecrire
        - to_highlight: (optionnel) [str] a chercher dans le message et a surligner
        """
        if to_highlight:
            m_to_highlight = f"{Style.BRIGHT}{self.CMD_HIGHLIGHT}{to_highlight}{Style.RESET_ALL}"
            print(f"{self.CMD_STANDARD}"
                  f"{message.replace(to_highlight, m_to_highlight)}"
                  f"{Style.RESET_ALL}")
        else:
            print(f"{self.CMD_STANDARD}{message}{Style.RESET_ALL}")

    def print_input(self, message, valueName, condition=lambda x: False, errorMessage=None):
        """
        Méthode générique pour demander à l'utilisateur d'entrer des informations

        parameters:
        - message: message à afficher avant l'entrée utilisateur
        - valueName: nom de la valuer a entrer pour l'utilisateur
        - condition: (optionnel) condition a remplir pour empecher de sortir de la boucle d'entrée
        - errorMessage: (optionnel) message à afficher si <condition> n'est pas respectée

        returns:
        - res: [str] de la saisi utilisateur
        """
        self.print_message(message)
        res = None
        while res is None or len(res) <= 0 or condition(res):
            if res is not None:
                self.print_error(errorMessage if errorMessage else "entree invalide")
            res = input(f"{valueName}: ")
        return res

    def print_table_node(self, node, cols=["title", "url"], showTable=True, toParentCD=".."):
        """
        Affiche un tableau representant l'ensemble des enfant contenant dans le noeud [node] selon les caracteristiques 
        selectionnee dans [cols]

        parameters:
        - node: [Node] dont afficher les enfants
        - cols: (optionnel) [list] des caracteristiques des noeuds enfants a afficher
        - showTable: (optionnel) [bool] affichant ou nan le tableau
        - toParentCD: (optionnel) cle associe au retour au parent

        returns:
        - res: [dict] associant {cle: noeud enfant} ou les cles sont des [int] sauf pour le parent qui est [toParentCD]
        """
        header = cols.copy()
        header.insert(0, "cd")
        header.insert(1, "type")
        table = []
        res = {}
        if node.parent is not None:
            node_object = vars(node.parent)
            current_line = [node_object[c] for c in header if
                            c in node_object.keys() and isinstance(node_object[c], str)]
            current_line.insert(0, toParentCD)
            current_line.insert(1, utils.get_node_type(node.parent))
            table.append(current_line)
            res[toParentCD] = node.parent
        compteur = 1
        for n in node.children:
            current_node_object = vars(n)
            current_line = [current_node_object[c] for c in header if
                            c in current_node_object.keys() and isinstance(current_node_object[c],
                                                                           str)]
            current_line.insert(0, compteur)
            current_line.insert(1, utils.get_node_type(n))
            table.append(current_line)
            res[str(compteur)] = n
            compteur += 1
        if len(table) > 0 and showTable:
            self.print_message(
                f"\n{self.CMD_HIGHLIGHT}{Style.BRIGHT}{utils.get_node_type(node)} {node.title}")
            print(tabulate(table, headers=header, tablefmt="fancy_grid", missingval="?"))
        return res

    def print_node_infos(self, infos):
        """
        Affiche les infos d'un noeud

        parameters:
        - infos: [dict] des infos du noeud
        """
        if infos is None:
            return
        for k in infos.keys():
            if isinstance(infos[k], str) and len(infos[k]) > 0:
                self.print_message(f"{k}: {infos[k]}", k)
            elif isinstance(infos[k], list):
                self.print_message(f"nb de {k}: {len(infos[k])}", f"nb de {k}")

    def print_regular_table(self, liste_obj, cols=None, title=None):
        """
        Affiche un tableau regulier sans retourner le dictionnaire des elements afficher

        parameters:
        - liste_obj: [list] des elements a afficher dans le tableau
        - cols: [list] des caracteristiques des elements a afficher
        - title: titre du tableau
        """
        header = cols.copy()
        if not header and len(liste_obj) > 0:
            header = liste_obj[0].keys()
        elif not header:
            return
        header.insert(0, "id")
        table = []
        compteur = 1
        for obj in liste_obj:
            current_line = [obj[k] for k in cols if
                            k in obj and isinstance(obj[k], str) and len(obj[k]) > 0]
            current_line.insert(0, compteur)
            table.append(current_line)
            compteur += 1
        if len(table) > 0:
            if title:
                self.print_message(f"\n{title}", title)
            print(tabulate(table, headers=header, tablefmt="fancy_grid", missingval="?"))


if __name__ == "__main__":
    printer = Printer()
    printer.print_help()
    printer.print_warning("presque mince...")
    printer.print_error("oh mince la catastrophe")
    test_video = Video("une url", "un titre", "un subtitle", "une description", "une durée",
                       "une date", "un thumbnail")
    print(vars(test_video))
    printer.print_table_node(test_video)
    print(type(test_video).__name__)
