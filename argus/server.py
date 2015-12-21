#! /usr/bin/python

"""
Tornado app for serving live file system events of watched directories,
using WebSocket
"""
from tornado import ioloop
from tornado import web

import settings
from handlers import argushandler


app = web.Application([
    (r'/ws/watch/(?P<path>.+)/?', argushandler.ArgusWebSocketHandler)
])

if __name__ == '__main__':
    print 'Starting Tornado IO loop at {}:{}'.format(
        settings.ARGUS_ADDRESS, settings.ARGUS_PORT
    )
    app.listen(settings.ARGUS_PORT, settings.ARGUS_ADDRESS)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print '\rClosing... (Interrupted by keyboard)'
