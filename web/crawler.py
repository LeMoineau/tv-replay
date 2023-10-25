# IMPORT: SYSTEM LIB
import os
import sys

# IMPORT: LIB
from helium import *
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
import time

# IMPORT: PROJECT
from web.utils.empty_element import EmptyElement

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Crawler:
    """
    Surcouche des driver selenium simplifie et reduit au minimum de fonction
    """
    
    def __init__(self, headless=True):
        self.driver = None
        self.headless = headless
        self.driverName = "Aucun"

    def init(self):
        """
        Initialise le crawler en lancer le driver firefox ou chrome en fonction des caracteristiques de l'ordinateur
        """
        try:
            self.driver = helium.start_firefox("duckduckgo.com", self.headless)
            self.driverName = "Mozilla Firefox"
        except Exception:
            print("firefox marche pas")
            try:
                self.driver = helium.start_chrome("duckduckgo.com", self.headless)
                self.driverName = "Google Chrome"
            except Exception as err:
                print("chrome marche pas")

        if not self.driver:
            raise Exception("Driver chrome et firefox ne fonctionne pas")

    def go_to(self, url):
        """
        Dirige le crawler vers la page a l'url donne

        parameters:
        - url: adresse du site ou aller
        """
        if "https://" not in url:
            url = f"https://{url}"
        self.driver.get(url)

    def execute_script(self, script, param=None):
        """
        Execute un script javascript dans la page courante en pouvant passer un parametre

        parameters:
        - script: [str] du script javascript a executer
        - param: (optionnel) element a envoyer en parametre dans le script javascript (accessible avec 'arguments[0]')

        returns:
        - res: resultat de l'execution du script javascript
        """
        return self.driver.execute_script(script, param)

    def move_to(self, element, delay=1):
        """
        Scroll la page courante sur l'element selectionne

        parameters:
        - element: element HTML sur lequel scroller dans la page
        - delay: (optionnel) delai d'attente (si animation speciale sur la page par exemple)
        """
        self.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(delay)

    def scroll_to_end_of_page(self, delay=0.5, increment=None):
        """
        Scroll jusqu'en bat de la page courante

        parameters:
        - delay: (optionnel) delai d'attente entre chaque scroll vers le bas
        - increment: (optionnel) [int] de pixel a scroller vers le bas
        """
        def generate_script(increment):
            if increment is None:
                return "window.scrollTo(0, document.body.scrollHeight);" \
                       "var lenOfPage=document.body.scrollHeight;return lenOfPage;"
            else:
                return f"window.scrollTo(0, {increment});" \
                       f"var lenOfPage=document.body.scrollHeight;return lenOfPage;"

        lenOfPage = self.driver.execute_script(generate_script(increment))
        match = False
        currentIncrement = increment
        while not match:
            lastCount = lenOfPage
            time.sleep(delay)
            if increment is not None:
                currentIncrement += increment
            lenOfPage = self.driver.execute_script(generate_script(currentIncrement))
            if increment is None and lastCount == lenOfPage:
                match = True
            elif increment is not None and currentIncrement >= lenOfPage:
                match = True

    def hover(self, element):
        """
        Passe la souris sur un element

        parameters:
        - element: element HTML sur lequel passer

        raises:
        - MoveTargetOutOfBoundsException: si l'element selectionne n'est pas affiche sur la page
        """
        try:
            self.move_to(element)
            helium.hover(element)
        except MoveTargetOutOfBoundsException:
            return

    def find_elements(self, expression="", parent=None):
        """
        Retourne la liste des elements correspondant a l'expression css donne dans le parent choisi

        parameters:
        - expression: selectionneur css
        - parent: (optionnel) element HTML dans lequel chercher, sinon cherchera dans toute la page courante

        returns:
        - res: liste des element HTML trouve pour la recherche courante
        """
        parent = self.driver if parent is None else parent

        try:
            return parent.find_elements_by_css_selector(expression)
        except NoSuchElementException:
            return []

    def find_element(self, expression="", parent=None):
        """
        Recherche l'element correspondant a l'expression donne et dans le parent choisi

        parameters:
        - expression: selectionneur css
        - parent (optionnel) element HTML dans lequel chercher, sinon cherchera dans toute la page

        returns: l'element HTML trouve ou [EmptyElement] si aucun trouve
        """
        res = self.find_elements(expression, parent)
        if len(res) > 0:
            return res[0]
        else:
            return EmptyElement()

    def find_html_element(self, expression, function_to_call=None, parent=None):
        """
        Recherche un element grace a une fonction javascript

        parameters:
        - expression: selectionneur css
        - function_to_call: (optionnel) [str] de fonction a appeler sur l'element trouve (exemple: textContent, innerHTML...etc)
        - parent: (optionnel) element HTML dans lequel chercher, sinon cherchera dans toute la page

        returns:
        - res: retour de la fonction javascript de recherche avec l'appel a la fonction [function_to_call] si utilise
        """
        return self.execute_script(
            f'let comp = arguments[0].querySelector("{expression}"); '
            f'return comp == null ? "" : comp.{function_to_call}', parent)


if __name__ == "__main__":
    c = Crawler()
    c.find_elements("a.coucou[id*='salut']")
