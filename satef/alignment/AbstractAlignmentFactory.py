from abc import ABC, abstractmethod
from alignment import AbstractAlignment

class AbstractAlignmentFactory(ABC):

    @abstractmethod
    def getAlignment(self) -> AbstractAlignment:
        pass

