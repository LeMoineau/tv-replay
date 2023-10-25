# IMPORT: SYSTEM LIB
import os
import sys

# IMPORT: LIB
import time
from datetime import datetime
import datetime
import uuid

# IMPORT: PROJECT
from elements.channel import Channel
from elements.categorie import Categorie
from elements.section import Section
from elements.video import Video
from web.utils.empty_element import EmptyElement

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


class ArteTV(Channel):
    def __init__(self):
        super().__init__("https://www.arte.tv/fr", guide_tv="https://www.arte.tv/fr/guide/",
                         title="ArteTV", headless=True)

    def _create_video_node(self, video_element):
        """
        Créer un noeud Video contenant toutes les informations standard trouvable sur le site ArteTV

        parameters
        - video_element: élément HTML déjà crawlé ayant l'attribut 'data-testid'='teaserItem' et contenant toutes les informations d'une vidéo

        returns:
        - Video: [Video] contenant url, titre, sous-titre, description, durée et thumbnail contenant dans le [video_element]
        """
        url = self.crawler.find_element("a", video_element).get_attribute("href")
        title = self.crawler.find_html_element("h3[id*='title']", "textContent", video_element)
        subtitle = self.crawler.find_html_element("p[id*='subtitle']", "textContent", video_element)
        description = self.crawler.find_html_element("p[id*='description']", "textContent",
                                                     video_element)
        duree = self.crawler.find_html_element("div[id*='duration'] > p", "textContent",
                                               video_element)
        thumbnail = self.crawler.find_element("img[data-testid='teaserImg']",
                                              video_element).get_attribute("src")
        return Video(url, title, subtitle, description, duree, "", thumbnail)

    def _section_scroll_to_right(self, section_element, max_click=15):
        """
        Scroll à droite dans une liste de vidéo sur le site ArteTV (élélement HTML avec l'attribut slider)

        parameters:
        - section_element: élément HTML dans lequel scroller à droite
        - max_click: limite de click pour pas trop ralentir l'app si la liste de vidéo est trop longue
        """
        selector = 'button[data-testid="next-arrow"]'
        next_button_exist = True
        compteur = 0
        while next_button_exist and compteur < max_click:
            next_button_exist = self.crawler.execute_script(
                f"return arguments[0].querySelector('{selector}') != null;", section_element)
            if next_button_exist:
                self.crawler.execute_script(
                    f"let comp = arguments[0].querySelector('{selector}'); if (comp != null) comp.click();",
                    section_element)
                time.sleep(0.5)
            compteur += 1

    def init(self):
        """
        Fonction d'initialisation de la classe [ArteTV] qui crawl la page d'acceuil du site
        """
        self.crawler.go_to("https://arte.tv/fr")
        menu_button = self.crawler.find_elements("button.css-kd1dms")
        if len(menu_button) >= 1:
            menu_button = menu_button[0]
            menu_button.click()
            cat_buttons = self.crawler.find_elements("a.css-4v7tsx, a.css-1192bg5")
            self.crawler.execute_script(
                "document.querySelector('.css-1d8a7ll').style.display = 'initial'")
            for c in cat_buttons:
                url = c.get_attribute("href")
                title = self.crawler.find_element("span", c).text
                self.add_child(Categorie(url, title))
        # self.crawl_categorie(self.get_child(url="https://www.arte.tv/fr/")) # (optionnel) crawl directement l'accueil (categorie à l'url de base)

    def crawl_categorie(self, categorie):
        """
        Crawl une categorie sur une page du site ArteTV

        parameters:
        - categorie: [Categorie] contenant l'url de la page a crawler pour cette categorie
        """
        if categorie.url == self.guide_tv:
            self.crawl_guide_tv(from_node=categorie)
            return
        self.crawler.go_to(categorie.url)
        self.crawler.scroll_to_end_of_page(increment=1000)
        sections = self.crawler.find_elements(
            "div.css-128d02j, div.css-1x8mgdm, .css-17ag8sr, .css-eh68r4")
        for s in sections:
            url = str(uuid.uuid4())
            title = self.crawler.find_element(
                "a[id*='_title'] > h2, h2[id*='_title'], h2.css-ld81nw, h2.css-c98hug", s).text
            description = self.crawler.find_element("p.css-1b5ywfs", s).text
            section = Section(url, title, s, description)
            categorie.add_child(section)
        if len(sections) <= 0:
            videos = self.crawler.find_elements("div[data-testid='teaserItem']")
            for v in videos:
                video = self._create_video_node(v)
                categorie.add_child(video)

    def crawl_section(self, section):
        """
        Crawl une section dans un page du site ArteTV

        parameters:
        - section: [Section] contenant l'element HTML de la section a crawler et dans lequel ajouter les nouveaux noeuds
        """
        self.crawler.move_to(section.html_element)
        self._section_scroll_to_right(section.html_element)
        videos = self.crawler.find_elements("div[data-testid='teaserItem']", section.html_element)
        for v in videos:
            video = self._create_video_node(v)
            section.add_child(video)

    def crawl_video(self, video):
        """
        Crawl une page de vidéo sur le site ArteTV

        parameters:
        - video: [Video] contenant l'url de la video a crawler et dans lequel on mettra tous les noeuds qu'on trouvera
        """
        self.crawler.go_to(video.url)
        videos_same_type = self.crawler.find_element("div.css-1t7m498")
        if not isinstance(videos_same_type, EmptyElement):
            videos_same_type_description = self.crawler.find_html_element("a[id*='title'] > h2",
                                                                          "textContent",
                                                                          videos_same_type)
            videos_same_type_section = Section(str(uuid.uuid4()), "Videos de la même série",
                                               videos_same_type, videos_same_type_description)
            video.add_child(videos_same_type_section)
        self.crawl_categorie(video)

    def crawl_research(self, query):
        """
        Crawl une recherche sur le site ArteTV

        parameters:
        - query: list de mots à rechercher
        """
        search_url = f"{self.url}/search/?q={'+'.join(query)}"
        search_cat = Categorie(search_url, title=f"Recherche - {' '.join(query)}")
        self.add_child(search_cat)
        self.crawl_categorie(search_cat)

    def crawl_guide_tv(self, date=None, from_node=None):
        """
        Crawl le guide tv pour une date donné sur le site ArteTV

        parameters:
        - date: (optionnel) [datetime] a laquelle crawler le programme tv. Si pas renseigné, devient la date d'aujourd'hui
        - from_node: (optionnel) [Node] parent depuis lequel a été lancé le crawling
        """
        if not date:
            date = datetime.date.today()
        datestr = date.strftime('%Y%m%d')
        date_bonformat = date.strftime('%d/%m/%Y')
        guide_tv_cat = Categorie(f"{self.url}/guide/{datestr}/", f"Guide TV du {date_bonformat}")
        if from_node:
            from_node.add_child(guide_tv_cat)
        else:
            self.add_child(guide_tv_cat)
        self.crawler.go_to(guide_tv_cat.url)
        previous_button = self.crawler.find_elements("button.previous-programs__button")
        if len(previous_button) > 0 and len(previous_button[0].text) > 0:
            previous_button[0].click()
        videos = self.crawler.find_elements("div.css-1k121lz-StyledProgram")
        for v in videos:
            url = self.crawler.find_element("a", v).get_attribute("href")
            title = self.crawler.execute_script(
                "let a = arguments[0].querySelector('.css-c21e1j-StyledProgramTitle'); let b = a.querySelector('.css-11xchxb'); if (b != undefined) a.removeChild(b); return a.textContent",
                v)
            subtitle = self.crawler.find_html_element("div[class*=StyledProgramSubTitle ]",
                                                      "textContent", v)
            description = self.crawler.find_html_element("div[class*=StyledProgramDescription]",
                                                         "textContent", v)
            date = date_bonformat + " à " + self.crawler.find_html_element(
                "span[class*=StyledProgramHour]", "textContent", v)
            thumbnail = self.crawler.find_element("img[class*=StyledImage]", v).get_attribute("src")
            guide_tv_cat.add_child(Video(url, title, subtitle, description, "", date, thumbnail))


if __name__ == "__main__":
    a = ArteTV()
    a.init()
    tmp = a.get_child(url="https://www.arte.tv/fr/")
    # print(tmp)
    # print(tmp.children[0])
    a.crawl_section(tmp.children[0])
    # print(tmp.children[0])
    a.crawl_guide_tv()
    guide_today = a.get_child(url="https://www.arte.tv/fr/guide/20220401/")
    print(guide_today)
    # print(str(a))
    a.dispose()
