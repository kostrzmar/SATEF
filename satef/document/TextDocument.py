from document import AbstractDocument, DocumentStats
from tools import FileUtils
import nltk 
import time


class TextDocument(AbstractDocument):

     def getDocumentStats(self):
        corpusReader = nltk.corpus.PlaintextCorpusReader( FileUtils.getParentPath(self.path_to_document), FileUtils.getFileFromPath(self.path_to_document))
        docStats = DocumentStats()
        docStats.nbr_sentences = len(corpusReader.sents())
        docStats.nbr_paragraphs = len(corpusReader.paras())
        docStats.nbr_words = len([word for sentence in corpusReader.sents() for word in sentence])
        docStats.nbr_characters = len([char for sentence in corpusReader.sents() for word in sentence for char in word])
        return docStats