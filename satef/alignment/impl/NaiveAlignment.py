from alignment import AbstractAlignment
from alignment.data import AlignmentMatch
#from document import TextDocument
from tools import FileUtils
from tools import ConfigConsts
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


class NaiveAlignment(AbstractAlignment):

    
    def getToolId(self):
        return 10

    def getOutputPrefix(self):
        return "NAIVE"


        
    def normalize(self, txt):
        #txt = "".join([c for c in txt if c (not in string.punctuation) or (not in stopwords.words('german'))])
        #
        #out = tokenizer.tokenize(txt)
        #out = [w for w in out if w not in stopwords.words('german')]
        out = ""
        tokenizer = RegexpTokenizer(r'\w+')
        for c in tokenizer.tokenize(txt):
            if c not in string.punctuation and c not in stopwords.words('german'):
                out = out + c + ' '
        return out

    def compareByWord(self, to_process, to_align):
        is_the_same = False
        tokenizer = RegexpTokenizer(r'\w+')
        to_process_as_array = tokenizer.tokenize(to_process)
        to_align_as_array = tokenizer.tokenize(to_align)
        for index in range(len(to_process_as_array)):
            word = to_process_as_array[index]
            if word not in string.punctuation and word not in stopwords.words('german'):
                if len(to_align_as_array) <= index or word != to_align_as_array[index]:
                    return is_the_same
        is_the_same = True
        return is_the_same


    def align(self):
        
        FileUtils.removeIfExit(self.output_file)
        with open(self.to_process.path_to_document) as f:
            to_process = f.readlines()
        with open(self.to_align.path_to_document) as f:
            to_align = f.readlines()
        for index_p, process_line in enumerate(to_process):
            for index_a, align_line in enumerate(to_align):
                if len(process_line.strip())>10 and len(align_line.strip())>10:
                    #if self.normalize(process_line.lower()) == self.normalize(align_line.lower()):
                    if self.compareByWord(process_line.lower(), align_line.lower()):
                        match = self.getAligmentMatch()
                        match.process_line_id = index_p
                        match.align_line_id = index_a
                        match.process_line = self.cleanTest(process_line.rstrip())
                        match.align_line = self.cleanTest(align_line.rstrip())
                        match.similarity = 100
                        self.alignment_matches.append(match)
        


        
                    
                    
                   
                  
        