#!/usr/bin/env python3
"""This is the main entrypoint to the application"""
import logging
import os
import cherrypy
from display.web import Web

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    conf = {
        'global': {
            'engine.autoreload.on': True
        },
        '/': {
            'tools.staticdir.root': os.path.dirname(__file__)
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    ss_path = os.path.join(os.path.dirname(__file__), "public", "img")
    web_server = Web(connected=True, screenshot_path=ss_path)
    try:
        web_server.start()
        cherrypy.engine.subscribe('stop', web_server.stop)
        cherrypy.quickstart(web_server, '/', config=conf)
    except KeyboardInterrupt:
        web_server.stop()
