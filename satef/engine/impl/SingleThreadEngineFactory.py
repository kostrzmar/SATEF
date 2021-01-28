from engine import AbstractEngineFactory
from engine import AbstractEngine
from engine.impl import SingleThreadEngine

class SingleThreadEngineFactory(AbstractEngineFactory):

    def getEngine(self) -> AbstractEngine:
        return SingleThreadEngine()