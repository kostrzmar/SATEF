from evaluation import AbstractEvaluationFactory
from evaluation import AbstractEvaluation
from evaluation.impl import BertScoreMetric

class BertScoreMetricFactory(AbstractEvaluationFactory):
 
    def getEvaluationMetric(self) -> AbstractEvaluation:
        return BertScoreMetric()