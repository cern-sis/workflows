class IExtractor:
    def __init__(self, destination):
        self.destination = destination

    def extract(self, root):
        raise NotImplementedError
