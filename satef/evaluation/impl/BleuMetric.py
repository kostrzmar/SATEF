from evaluation import AbstractEvaluation
from alignment.data import AlignmentMatch
from nltk.translate.bleu_score import sentence_bleu


class BleuMetric(AbstractEvaluation):

    def getMetricName(self):
        return "BLEU (nltk)"


    def evaluate(self, alignmentMatches):
        for alignmentMatch in alignmentMatches:
            alignmentMatch.addEvalationMetricResult(self.getMetricName(), 
                sentence_bleu(  alignmentMatch.process_line, alignmentMatch.align_line)
            )
        