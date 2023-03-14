import random
import string
import cherrypy
from jinja2 import Environment, FileSystemLoader
from clock import Clock

class Web(object):
    """
    Web manages the web interface for the display.
    """
    def __init__(self):
        self._environment = Environment(loader=FileSystemLoader("templates/"))
        self.clock = Clock()

    @cherrypy.expose
    def start(self):
        self.clock.start()
        return "started"

    @cherrypy.expose
    def stop(self):
        self.clock.stop()
        return "stopped"

    @cherrypy.expose
    def index(self):
        template = self._environment.get_template("index.html")
        return template.render(
            mode=self.clock.get_state()
        )

    @cherrypy.expose
    def generate(self):
        return ''.join(random.sample(string.hexdigits, 8))

    @cherrypy.expose
    def control(self, action):
        return action
