from evaluation import AbstractEvaluation
from alignment.data import AlignmentMatch
from nltk.translate.meteor_score import meteor_score


class MeteorMetric(AbstractEvaluation):

    def getMetricName(self):
        return "METEOR (nltk)"


    def evaluate(self, alignmentMatches):
        for alignmentMatch in alignmentMatches:
            alignmentMatch.addEvalationMetricResult(self.getMetricName(), 
                meteor_score(alignmentMatch.process_line, alignmentMatch.align_line)
            )
        