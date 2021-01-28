from abc import ABC, abstractmethod

class AbstractDocument(ABC):
    """ Abstract document class """

    def __init__(self, pathToDocument):
        self.path_to_document = pathToDocument
        super().__init__()

    @abstractmethod
    def getDocumentStats(self):
        pass