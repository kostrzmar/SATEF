from evaluation import AbstractEvaluationFactory
from evaluation import AbstractEvaluation
from evaluation.impl import MeteorMetric

class MeteorMetricFactory(AbstractEvaluationFactory):
 
    def getEvaluationMetric(self) -> AbstractEvaluation:
        return MeteorMetric()