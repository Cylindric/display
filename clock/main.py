import logging
import os
import cherrypy
from web import Web

logging.basicConfig(level=logging.DEBUG)

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

    web_server = Web()
    try:
        web_server.start()
        cherrypy.engine.subscribe('stop', web_server.stop)
        cherrypy.quickstart(web_server, '/', config=conf)
    except KeyboardInterrupt:
        web_server.stop()
