import cherrypy
import logging
import os
import random
import string
from jinja2 import Environment, FileSystemLoader
from ClockController import Clock

logging.basicConfig(level=logging.DEBUG)

class HelloWorld(object):
    
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


if __name__ == '__main__':
    conf = {
        'global': {
            'engine.autoreload.on': True
        },
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    H = HelloWorld()
    H.start()
    try:
        cherrypy.engine.subscribe('stop', H.stop)
        cherrypy.quickstart(H, '/', config=conf)
    except KeyboardInterrupt:
        H.stop()
