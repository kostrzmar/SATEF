from evaluation import AbstractEvaluationFactory
from evaluation import AbstractEvaluation
from evaluation.impl import RougeMetric

class RougeMetricFactory(AbstractEvaluationFactory):
 
    def getEvaluationMetric(self) -> AbstractEvaluation:
        return RougeMetric()