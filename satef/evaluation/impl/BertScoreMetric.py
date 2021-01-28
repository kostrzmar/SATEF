from evaluation import AbstractEvaluation
from alignment.data import AlignmentMatch
from tools import ConfigConsts
import bert_score


class BertScoreMetric(AbstractEvaluation):

    def getMetricName(self):
        return "BertScore"

    def evaluate(self, alignmentMatches):
        process_line = []
        align_line = []
        for alignmentMatch in alignmentMatches:
            process_line.append(alignmentMatch.process_line)
            align_line.append(alignmentMatch.align_line)

        all_preds, hashBert = bert_score.score(
            process_line, 
            align_line, 
            model_type=self.local_config_utils.getValue(ConfigConsts.CONF_SEC_EVALUATION, ConfigConsts.CONF_METRICS_BERT_SCORE_MODEL, "bert-base-multilingual-cased"), 
            idf=False, 
            return_hash=True, 
            verbose=False)
        for P, R, F1, alignmentMatch in zip (all_preds[0].tolist(),  all_preds[1].tolist(), all_preds[2].tolist(), alignmentMatches):
            alignmentMatch.addEvalationMetricResult(self.getMetricName()+"_Hash", hashBert)
            alignmentMatch.addEvalationMetricResult(self.getMetricName()+"_P", P)
            alignmentMatch.addEvalationMetricResult(self.getMetricName()+"_R", R)
            alignmentMatch.addEvalationMetricResult(self.getMetricName()+"_F1", F1)
        
        