from twisted.application import service


class ThreadPoolService(service.Service):
    """
    ThreadPoolService class implementing a ThreadPool as a
    Twisted Service
    """
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()
