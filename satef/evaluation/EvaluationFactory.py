from tools import ConfigConsts
from evaluation import AbstractEvaluation
from evaluation.impl import BleuMetricFactory, MeteorMetricFactory, RougeMetricFactory, BertScoreMetricFactory

class EvaluationFactory:

    def getEvaluations(self, config_utils : ConfigConsts) -> list:
        assert config_utils ,"Configuration is empty"
        evaluationMetrics = []
        metrics = config_utils.getValue(ConfigConsts.CONF_SEC_EVALUATION, ConfigConsts.CONF_METRICS)
        for metric in metrics:
            evaluationFactory = None 
            if metric == 'BLEU':
                evaluationFactory = BleuMetricFactory()
            elif metric == 'METEOR':
                evaluationFactory = MeteorMetricFactory()
            elif metric == 'ROUGE':
                evaluationFactory = RougeMetricFactory()
            elif metric == 'BERT_SCORE':
                evaluationFactory = BertScoreMetricFactory()

            if evaluationFactory:
               metric = evaluationFactory.getEvaluationMetric()
               metric.setConfigUtils(config_utils) 
               evaluationMetrics.append(metric) 
        return evaluationMetrics 