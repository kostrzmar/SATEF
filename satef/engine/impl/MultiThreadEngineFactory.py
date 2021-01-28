from engine import AbstractEngineFactory
from engine import AbstractEngine
from engine.impl import MultiThreadEngine

class MultiThreadEngineFactory(AbstractEngineFactory):

    def getEngine(self) -> AbstractEngine:
        return MultiThreadEngine()