from .sampling import Sampler

class Service:
    def __init__(self):
        self.sampler = Sampler()

    def start(self):
        self.sampler.start()
        return self

    def stop(self):
        self.sampler.stop()
        return self