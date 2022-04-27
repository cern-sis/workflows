class IExtractor:
    def __init__(self, destination) -> None:
        self.destination = destination

    def extract(self, root):
        raise NotImplementedError
