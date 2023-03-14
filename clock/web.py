"""This module provides management for the Web interface"""
import cherrypy
from jinja2 import Environment, FileSystemLoader
from dashboard import Dashboard

class Web():
    """
    Web manages the web interface for the display.
    """
    def __init__(self, connected=True):
        """Instantiates the Web class

        Args:
            connected (bool, optional): set to false to run without an attached screen.
                                        Defaults to True.
        """
        self._environment = Environment(loader=FileSystemLoader("templates/"))
        self._dashboard = Dashboard(connected=connected)

    @cherrypy.expose
    def start(self):
        self._dashboard.start()
        return "started"

    @cherrypy.expose
    def stop(self):
        self._dashboard.stop()
        return "stopped"

    @cherrypy.expose
    def index(self):
        template = self._environment.get_template("index.html")
        return template.render(
            mode=self._dashboard.get_clock_state()
        )

    # @cherrypy.expose
    # def generate(self):
    #     return ''.join(random.sample(string.hexdigits, 8))

    # @cherrypy.expose
    # def control(self, action):
    #     return action
