# TV Replay

TV-Replay est une application python Open-Source qui permet de télécharger facilement des vidéos depuis plusieurs sites de streaming français.

A l'heure actuelle, TV-Replay peut télécharger des vidéos depuis les sites suivants:
- Arte

## Installation

Pour installer TV-Replay suivez les instructions suivantes:
- `git clone https://github.com/LeMoineau/tv-replay.git`
- ouvrir un terminal dans le repertoire nouvellement créé
- `pip install bs4 argcomplete tabulate helium PySide6 youtube_dl`
- `python3 main.py -h`

### Lancement TV-Replay version terminal

- `python3 main.py` ou `python3 cli/cli.py`

### Lancement TV-Replay version web

- `python3 main.py gui` ou `python3 ui/server.py` *cette commande va lancé un serveur en local*
- entrer l'url `localhost:5000` ou `127.0.0.1:5000` dans un navigateur internet

## Requirements

Pour fonctionner, ce projet a besoin de:
- python3

## Dependances 

library python préinstallés
- re
- requests
- argparse
- os
- sys
- hashlib
- colorama

library python opensources
- argcomplete
- tabulate
- helium (selenium)
- beautiful_soup_4 (bs4)
- youtube-dl
- PySide6
- flask
