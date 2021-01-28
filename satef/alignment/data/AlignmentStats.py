from tools import FileUtils
import numpy as np
class AlignmentStats():
        
    def __init__(self):
        self.file_name = 0
        self.process_sentence_nbr =0 
        self.align_sentence_nbr = 0
        self.process_paragraph_nbr =0 
        self.align_paragraph_nbr = 0   
        self.process_word_nbr =0 
        self.align_word_nbr = 0   
        self.process_char_nbr =0 
        self.align_char_nbr = 0 
        self.total_alignment_nbr = 0  
        self.mean_score = 0
        self.var_score = 0
        self.stddev_score = 0
        super().__init__()

    def initialize(self, outputFile, procDocStats, alignDocStats, alignmentMatches):
        self.file_name  = FileUtils.getFileFromPath(outputFile)
        self.process_sentence_nbr = procDocStats.nbr_sentences
        self.align_sentence_nbr = alignDocStats.nbr_sentences
        self.process_paragraph_nbr = procDocStats.nbr_paragraphs
        self.align_paragraph_nbr = alignDocStats.nbr_paragraphs 
        self.process_word_nbr = procDocStats.nbr_words
        self.align_word_nbr = alignDocStats.nbr_words   
        self.process_char_nbr = procDocStats.nbr_characters
        self.align_char_nbr = alignDocStats.nbr_characters
        self.total_alignment_nbr =  len(alignmentMatches)

        if len(alignmentMatches)>0:
            values = []
            for m in alignmentMatches:
                values.append(m.similarity)
            floatlist = np.array(values, np.float)
            self.mean_score = np.mean(floatlist)
            self.var_score = np.var(floatlist)
            self.stddev_score = np.std(floatlist)

     
    def getHeaders(self):
        return [
            "File",
            "Org SentNbr",
            "Trg SentNbr",
            "Org ParNbr",
            "Trg ParNbr", 
            "Org WordNbr",
            "Trg WordNbr",
            "Org charNbr",
            "Trg charNbr",
            "Total AlgNbr",
            "Mean Score",
            "Var Score",
            "StdDev Score"
        ]

    def getValues(self):
        return [
        self.file_name,
        self.process_sentence_nbr,
        self.align_sentence_nbr,
        self.process_paragraph_nbr,
        self.align_paragraph_nbr,
        self.process_word_nbr,
        self.align_word_nbr,
        self.process_char_nbr,
        self.align_char_nbr,
        self.total_alignment_nbr, 
        self.mean_score,
        self.var_score,
        self.stddev_score,
        ]