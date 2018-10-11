from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from PikcioChain import init_api_client
from config import get_config


def run():
    config = get_config()
    app = init_api_client()
    flask_site = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(flask_site)

    reactor.listenTCP(config.get('application', 'port'), site)
    reactor.run()
