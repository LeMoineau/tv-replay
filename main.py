# IMPORT: PROJECT
from cli.parser import Parser
from cli.client import Client

from ui.server import app

if __name__ == "__main__":
    parser = Parser()
    parser.init()

    if parser.get_arg("gui"):
        app.run()
    else:
        client = Client(parser)
        client.run()
