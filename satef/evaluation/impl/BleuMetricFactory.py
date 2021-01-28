from evaluation import AbstractEvaluationFactory
from evaluation import AbstractEvaluation
from evaluation.impl import BleuMetric

class BleuMetricFactory(AbstractEvaluationFactory):
 
    def getEvaluationMetric(self) -> AbstractEvaluation:
        return BleuMetric()