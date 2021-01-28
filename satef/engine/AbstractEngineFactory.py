from abc import ABC, abstractmethod
from engine import AbstractEngine
class AbstractEngineFactory(ABC):
    
    @abstractmethod
    def getEngine(self) -> AbstractEngine:
        pass
