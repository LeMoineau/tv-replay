# Replay TV - Interface web

Interface web pour l'application Replay TV

## Lancement

- `pip install flask`, *si pas déjà installé*
- `python3 server.py`
- sur un navigateur internet, taper l'url `localhost:5000`

## Arborescence site Replay TV

- server.py
- templates/
    - *.html
- static/
    - assets/images/
        - *.png
        - *.jpg
    - css/
        - *.css
    - js/
        - *.js

## Conventions de codage web

### Style

- séparer le style de chaque gros composant du site dans des fiches de style (fichier `.css` différents)
- mettre les paramètres des gros composants comme `var(--XXX)` dans le fichier `static/css/global.css` (voir la propriété `:root` du fichier)
- le noms des `class` et des `#id` doit etre descendant avec les elements HTML
- utiliser à fond les flex-box mais le moins possible de propriété static (position: absolute, margin/padding pour le position)

*exemple*:
- div.nav-button
    - img.nav-button-icon
    - p.nav-button-title
        - span.nav-button-title-truc

### Javascript

- noms des variables, fonction ...etc en `camelCase`