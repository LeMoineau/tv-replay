# IMPORT: SYSTEM LIB
import os
import sys

# IMPORT: LIB
from flask import Flask, render_template, jsonify, request

# IMPORT: PROJECT
from ui.webController import WebController

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Serveur flask
app = Flask(__name__)

# url racine du projet
base_url = os.path.dirname(__file__)

# Manager des evenements des appels AJAX au serveur
webController = WebController()


@app.route("/")
def main():
    """
    Affiche la page d'acceuil de l'interface graphique de Replay TV

    returns:
    - template: page 'index.html' de l'interface graphique
    """
    return render_template("index.html")


@app.route("/channel", methods=["GET"])
def channel():
    """
    Créer un noeud racine pour la chaine selectionnee et renvoie les informations de ce noeud

    parameters:
    - name: [request.args] nom de la chaine a crawler

    returns:
    - json: json des informations du noeud de la chaine selectionnee
    """
    res = webController.crawl_channel(request.args["name"])
    return jsonify({"channel": res})


@app.route("/node", methods=["GET"])
def node():
    """
    Cherche tous les enfants du noeud selectionne et renvoie les informations concernant ce noeud

    parameters:
    - id: [request.args] id du noeud pour lequel recuperer les enfants et les infos

    returns:
    - json: json des informations du noeud (contenant la liste des enfants du noeud)
    """
    id = request.args["id"]
    res = webController.crawl_node(id)
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
