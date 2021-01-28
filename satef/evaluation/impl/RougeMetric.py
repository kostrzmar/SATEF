from evaluation import AbstractEvaluation
from alignment.data import AlignmentMatch
from rouge import Rouge 


class RougeMetric(AbstractEvaluation):

    def getMetricName(self):
        return "Rouge"


    def evaluate(self, alignmentMatches):
        rouge = Rouge()
        for alignmentMatch in alignmentMatches:
            score = rouge.get_scores( alignmentMatch.process_line, alignmentMatch.align_line)
            for rogueScore in score:
                for key in rogueScore.keys():
                    alignmentMatch.addEvalationMetricResult(key, rogueScore.get(key))
        