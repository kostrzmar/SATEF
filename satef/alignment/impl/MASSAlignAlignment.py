
from nltk.corpus import stopwords
from massalign.core import TFIDFModel, VicinityDrivenParagraphAligner, VicinityDrivenSentenceAligner, MASSAligner
from alignment import AbstractAlignment
from alignment.data import AlignmentMatch
from document import TextDocument
from tools import FileUtils
from tools import ConfigConsts

class MASSAlignAlignment(AbstractAlignment):


# download https://github.com/ghpaetzold/massalign
# install 2to3 -> pip3 install 2to3
# convert to python 3 -> 2to3 . -w
# install package -> python setup.py install

    
    def getToolId(self):
        return 20

    def getOutputPrefix(self):
        return "MASSALIGN"

    def align(self):    
        FileUtils.removeIfExit(self.output_file)
        model = TFIDFModel([self.to_process.path_to_document, self.to_align.path_to_document], stopwords.abspath(self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_MASSALIGN_STOP_WORDS)))
        paragraph_aligner = VicinityDrivenParagraphAligner(similarity_model=model, acceptable_similarity=float(self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_MASSALIGN_PARAGRAPH_ACCEPTABLE_SIMILARITY)))
        sentence_aligner = VicinityDrivenSentenceAligner(similarity_model=model, acceptable_similarity=float(self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_MASSALIGN_SENTENCE_ACCEPTABLE_SIMILARITY)), similarity_slack=float(self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_MASSALIGN_SENTENCE_SIMILARITY_SLACK)))
        m = MASSAligner()
        p1s = m.getParagraphsFromDocument(self.to_process.path_to_document)
        p2s = m.getParagraphsFromDocument(self.to_align.path_to_document)
        alignments, aligned_paragraphs = m.getParagraphAlignments(p1s, p2s, paragraph_aligner)
        for a, b in zip(aligned_paragraphs, alignments):
            p1 = a[0]
            p2 = a[1]
            alignments, aligned_sentences = m.getSentenceAlignments(p1, p2, sentence_aligner)
            for a, b in zip(alignments, aligned_sentences):
                match = self.getAligmentMatch()
                match.process_line_id = a[0]
                match.align_line_id = a[1]
                match.process_line = self.cleanTest(b[0].rstrip())
                match.align_line = self.cleanTest(b[1].rstrip())
                match.similarity = model.getTextSimilarity(match.process_line, match.align_line)
                self.alignment_matches.append(match)        
