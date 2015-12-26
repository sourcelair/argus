"""
Argus websocket handler and event handler
"""
import os
from re import sub
from json import dumps
from tornado import ioloop
from tornado import websocket
from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer

from settings import ARGUS_ROOT


active_handlers = {}
active_observers = {}


class Argus(RegexMatchingEventHandler):
    def __init__(self, web_socket, root, *args, **kwargs):
        super(Argus, self).__init__(*args, **kwargs)
        self.websockets = [web_socket]
        self.root = root

    def write_msg(self, message):
        for wbsocket in self.websockets:
            wbsocket.write_message(message)

    def on_created(self, event):
        self.write_msg(
            dumps(
                {
                    'event_type': 'created',
                    'is_directory': event.is_directory,
                    'src_path': sub(self.root, '', event.src_path)
                }
            )
        )

    def on_modified(self, event):
        self.write_msg(
            dumps(
                {
                    'event_type': 'modified',
                    'is_directory': event.is_directory,
                    'src_path': sub(self.root, '', event.src_path)
                }
            )
        )

    def on_deleted(self, event):
        self.write_msg(
            dumps(
                {
                    'event_type': 'deleted',
                    'is_directory': event.is_directory,
                    'src_path': sub(self.root, '', event.src_path)
                }
            )
        )

    def on_moved(self, event):
        self.write_msg(
            dumps(
                {
                    'event_type': 'moved',
                    'is_directory': event.is_directory,
                    'src_path': sub(self.root, '', event.src_path),
                    'dest_path': sub(self.root, '', event.dest_path)
                }
            )
        )

    def add_socket(self, wbsocket):
        self.websockets.append(wbsocket)

    def remove_socket(self, wbsocket):
        if wbsocket in self.websockets:
            self.websockets.remove(wbsocket)


class ArgusWebSocketHandler(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(ArgusWebSocketHandler, self).__init__(*args, **kwargs)
        self.started_observer = False
        self.observer = None
        self.path = None
        self.args = []
        self.kwargs = {}

    def check_origin(self, origin):
        return True

    def initiation_handler(self):
        """
        Observers are unique per watched path.
        If an observer already exists for the requested path,
        the new web socket is added in the observer's sockets via the
        handler.
        In order to achieve this, both the handler and the observer objects
        are stored in a global dict.
        """
        self.path = os.path.join(ARGUS_ROOT, self.kwargs.get('path'))
        if not os.path.exists(self.path):
            self.write_message('Path does not exist.')
            self.close()
            return
        if self.path in active_observers:
            event_handler = active_handlers[self.path]
            event_handler.add_socket(self)
            self.observer = active_observers[self.path]
            self.started_observer = True
        else:
            event_handler = Argus(
                web_socket=self, root=self.path,
                case_sensitive=True
            )
            self.observer = Observer()
            self.observer.schedule(
                event_handler, path=self.path, recursive=True
            )
            print '- Starting fs observer for path {}'.format(self.path)
            try:
                self.observer.start()
            except OSError:
                self.write_message('Cannot start observer')
                self.close()
                return
            active_handlers[self.path] = event_handler
            active_observers[self.path] = self.observer
            self.started_observer = True

    def open(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.callback = ioloop.PeriodicCallback(lambda: self.ping(''), 60000)
        self.callback.start()
        self.initiation_handler()

    def on_message(self, message):
        pass

    def data_received(self, chunk):
        pass

    def on_close(self):
        self.callback.stop()
        if self.started_observer:
            event_handler = active_handlers[self.path]
            event_handler.remove_socket(self)
            if event_handler.websockets == []:
                print '- Stopping fs observer'
                self.observer.stop()
                del active_observers[self.path]
                del active_handlers[self.path]
