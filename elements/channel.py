# IMPORT: LIB
from abc import abstractmethod
import helium

# IMPORT: PROJECT
from elements.node import Node
from web.crawler import Crawler


class Channel(Node):
    """
    Noeud racine representant un site

    attributes:
    - guide_tv: [str] du lien du programme TV du site
    - crawler: [Crawler] associe au site courant
    """
    
    def __init__(self, url, guide_tv, title=None, headless=False):
        super().__init__(url, title, [])

        self.guide_tv = guide_tv
        self.crawler = Crawler(headless=headless)
        self.crawler.init()

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def crawl_categorie(self, categorie):
        pass

    @abstractmethod
    def crawl_section(self, section):
        pass

    @abstractmethod
    def crawl_video(self, video):
        pass

    @abstractmethod
    def crawl_research(self, query):
        pass

    @abstractmethod
    def crawl_guide_tv(self, date):
        pass

    def dispose(self):
        helium.kill_browser()

    def __str__(self):
        res = f"<channel, " \
              f"url='{self.url}', " \
              f"name='{self.title}', l" \
              f"en_children={len(self.children)}>"

        for c in self.children:
            res += f"\n{str(c)}"
        return res
