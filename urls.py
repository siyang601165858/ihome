import os

from handlers.basehandler import StaticFileHandler

urls = [

    (r"/(.*)", StaticFileHandler,
     {"path": os.path.join(os.path.dirname(__file__), "html"), "default_filename": "index.html"})

]