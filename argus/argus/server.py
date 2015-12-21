#! /usr/bin/python

"""
Tornado app for serving live file system events of watched directories,
using WebSocket
"""
from tornado import ioloop
from tornado import web

from argus import settings
from handler import ArgusWebSocketHandler


def make_app():
    """
    Creates tornado application which routes incoming requests to handlers
    """
    return web.Application(
        [
            (r'/ws/watch/(?P<path>.+)/?', ArgusWebSocketHandler),
        ]
    )


def runserver():
    """
    Starts server at ARGUS_ADDRESS:ARGUS_PORT given by the settings.
    """
    print 'Starting Tornado IO loop at {}:{}'.format(
        settings.ARGUS_ADDRESS, settings.ARGUS_PORT
    )
    app = make_app()
    app.listen(settings.ARGUS_PORT, settings.ARGUS_ADDRESS)
    try:
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print '\rClosing... (Interrupted by keyboard)'


if __name__ == '__main__':
    runserver()
