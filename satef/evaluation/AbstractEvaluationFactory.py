from abc import ABC, abstractmethod
from evaluation import AbstractEvaluation

class AbstractEvaluationFactory(ABC):

    @abstractmethod
    def getEvaluationMetric(self) -> AbstractEvaluation:
        pass

