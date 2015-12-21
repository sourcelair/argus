#! /usr/bin/python

"""
Tornado app for serving live file system events of watched directories,
using WebSocket
"""
from tornado import ioloop
from tornado import web

import settings
from handlers import argushandler


def make_app():
    """
    Creates tornado application which routes incoming requests to handlers
    """
    return web.Application(
        [
            (r'/ws/watch/(?P<path>.+)/?', argushandler.ArgusWebSocketHandler),
        ]
    )


def main():
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
    main()
