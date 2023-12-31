# IMPORT: SYSTEM LIB
import os
import sys

# IMPORT: LIB
import argcomplete
import argparse

# IMPORT: PROJECT
from enums import enum_site

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Parser(object):
    """
    Classe generant les parametres pouvant etre donne et donne lors de l'execution du script main de replay-tv

    attributes:
    - title: titre afficher dans le menu d'aide du script python
    - parser: [ArgumentParser] associe au [Parser] courant
    """

    def __init__(self, title="Ensemble des commandes du programme TV-Replay"):
        self.title = title
        self.parser = argparse.ArgumentParser(description=self.title, epilog="")

    def init(self):
        """
        Initialise la gestion des arguments pour le parser
        """
        self._add_args()
        self._apply_parser()

    def _add_args(self):
        """
        Ajoute tous les parametres à la commande d'execution (-s, -c ...etc)
        """
        # optional args
        subparsers = self.parser.add_subparsers()
        tmp_parser = subparsers.add_parser("gui", help=f"ouvrir l'interface graphique")
        tmp_parser.set_defaults(gui=True)
        tmp_parser = subparsers.add_parser("cli", help=f"lancer l'interface terminal")
        tmp_parser.set_defaults(cli=True)

        # create the parser for the "a" command
        self.parser.add_argument("-s", "--site", metavar="SITE", choices=set(enum_site.keys()),
                                 help="site source", nargs=1)

    def _apply_parser(self):
        """
        Applique les arguments ajouté au parser pour le terminal
        """
        argcomplete.autocomplete(self.parser)
        self.args = vars(self.parser.parse_args())

    def print_help(self):
        """
        Affiche les aides de la commande dans le terminal
        """
        self.parser.print_help()

    def get_arg(self, name):
        """
        Renvoie l'argument <name> demandé

        parameters:
        - name: nom de l'argument à renvoyer

        returns:
        - arg: argument de nom <name>
        """
        if name in self.args:
            arg = self.args[name]
            if isinstance(arg, list) and len(arg) == 1:
                return arg[0]
            return arg
        return None

    def has_arg(self, name):
        """
        Vérifie si le parser contient l'argument <name>

        parameters:
        - name: nom de l'argument à verifier

        returns:
        - bool: parser contient l'argument ou non
        """
        return self.get_arg(name) is not None


if __name__ == "__main__":
    parser = Parser()
    parser.init()
    parser.print_help()
    print(parser.args)
    print(f"arg 'site': {parser.get_arg('site')}")
    print(f"arg 'query': {parser.get_arg('query')}")
    print(f"arg 'gui': {parser.get_arg('gui')}")
