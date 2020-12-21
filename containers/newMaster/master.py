import eventlet
import socketio
import logging

from logger import get_logger
from registry import Registry, RegistryNamespace
from datatype import Master, NodeSpecs
from message import Message


class FogMaster:

    def __init__(self, host: str, port: int, logger=logging):
        self.host = host
        self.port = port
        self.sio = socketio.Server()
        self.registry = Registry()
        self.logger = get_logger('Master', logging.INFO)

    def run(self):

        app = socketio.WSGIApp(self.sio, static_files={
            '/': {'content_type': 'text/html', 'filename': 'html/index.html'}
        })
        self.sio.register_namespace(RegistryNamespace(
            '/registry', registry=self.registry, sio=self.sio, logLevel=self.logger.level))

        eventlet.wsgi.server(eventlet.listen((self.host,  self.port)),
                             app, log=get_logger("EventLet", logging.DEBUG), log_output=False)
        self.logger.info("[*] Master serves at: %s:%d" %
                         (self.host,  self.port))


if __name__ == '__main__':
    master = FogMaster('', 5000)
    master.run()
