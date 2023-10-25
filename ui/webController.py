# IMPORT: SYSTEM LIB
import os
import sys

# IMPORT: PROJECT
from ui.utils import node_to_json
from enums import enum_site

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class WebController:
    def __init__(self):
        self.tree = {}

    def crawl_channel(self, channelName):
        site_class = enum_site[channelName]["crawler"]()
        self.tree[channelName] = site_class
        site_class.init()
        return node_to_json(site_class)

    def crawl_node(self, id):
        node, channel = self.get_node(id)
        if node:
            getattr(self.tree[channel], f"crawl_{node.get_type_str().lower()}")(node)
            return node_to_json(node)
        return {"error": f"pas de noeud trouvé pour l'id {id}"}

    def get_node(self, id):
        for channel in self.tree:
            node = self.tree[channel].get_child(id=id)
            if node:
                return node, channel
        return None, None

    def dispose(self):
        for c in self.tree.keys():
            self.tree[c].dispose()


if __name__ == "__main__":
    wController = WebController()
    wController.crawl_channel("arte")
    print(wController.tree)
    print(wController.tree["arte"])
    wController.dispose()
