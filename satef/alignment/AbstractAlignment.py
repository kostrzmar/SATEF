from abc import ABC, abstractmethod
from alignment.data import AlignmentStats, AlignmentMatch
from document import TextDocument
from tools import ConfigConsts
from tools import ConfigUtils
from tools import FileUtils
from pathlib import Path
import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
import os
import re 

import csv
from distutils.util import strtobool
    
from functools import wraps
from multiprocessing import Process, Queue


class AbstractAlignment(ABC):


    #def __init__(self, config_parser, to_process, to_align, direction_prefix, unique_processing_stats_file_name, **kwargs):
    def __init__(self):
        self.local_config_utils = None
        self.id = None
        self.prefix = None
        self.direction_prefix = None
        self.output_folder =  None
        self.to_process = None
        self.to_align = None
        self.output_file = None
        self.unique_processing_id = None
        self.processing_stats_file = None
        self.key_word_argument = None
        self.alignment_matches = []
        self.evaluations = []
        super().__init__()

    
    def initialize(self, config_utils : ConfigUtils, to_process, to_align, direction_prefix, unique_processing_id, evaluations,  **kwargs) -> None:
        self.local_config_utils = config_utils
        self.id = self.getToolId()
        self.prefix = self.getOutputPrefix()
        self.unique_processing_id = unique_processing_id
        self.direction_prefix = direction_prefix
        self.output_folder =  self.getConfigValue(ConfigConsts.CONF_SEC_ALIGNMENT, ConfigConsts.CONF_ALIGNMENT_OUTPUT_PATH) 
        self.to_process = TextDocument(to_process)
        self.to_align = TextDocument(to_align)
        self.evaluations = evaluations
        self.output_file = self.getOutputFile()
        self.processing_stats_file = self.getProcessingStatsFile()
        self.key_word_argument = kwargs
        self.makeOutputFolder()
    


    
    @abstractmethod
    def getToolId(self):
        pass
   
    @abstractmethod
    def getOutputPrefix(self):
        pass

    def getToolSecName(self):
        return ConfigConsts.CONF_SEC_ALIGNMENT
    
    @abstractmethod
    def align(self):
        pass

    def evaluate(self):
        if len(self.alignment_matches)>0:
            for evaluator in self.evaluations:
                evaluator.evaluate(self.alignment_matches)


    def doAlignment(self):
        self.align()
        self.evaluate()
        self.storeMatches()
        self.storeStatistic()

    def getOutputDirectory(self):
        return os.path.join(self.output_folder, self.unique_processing_id, self.prefix, self.direction_prefix)

    def getAbsoluteFileName(self, fileName):
        return os.path.join(self.getOutputDirectory(), fileName)

    def getProcessingStatsFile(self):
        return self.getAbsoluteFileName("processing_statistic.csv")
    
    def getAligmentMatch(self):
        match = AlignmentMatch()
        match.tool_id = self.getToolId()
        return match

    def makeOutputFolder(self):
        path = Path(self.output_file)
        path.parent.mkdir(parents=True, exist_ok=True) 

    def getConfigValue(self, section, key):
        return self.local_config_utils.getValue(section,key)

    def getOutputFile(self):
        fileOutFileName = FileUtils.getFileFromPath(self.to_process.path_to_document) + "_vs_" + FileUtils.getFileFromPath(self.to_align.path_to_document)+ "_alignment.csv"
        return self.getAbsoluteFileName( fileOutFileName)
    
    def cleanTest(self, stringToCleanup):
        chars = ";\"'"
        for c in chars:
            stringToCleanup = stringToCleanup.replace(c, ' ')
        return stringToCleanup

    def storeMatches(self):
        if len(self.alignment_matches)>0:
            with open(self.output_file, 'a+',encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=';', escapechar='/', quoting=csv.QUOTE_NONE)
                writer.writerow(self.alignment_matches[0].getHeaders())
                for match in self.alignment_matches:
                    writer.writerow(match.getValues())

    def storeStatistic(self):
        stats = AlignmentStats()
        stats.initialize(self.output_file, 
            self.to_process.getDocumentStats(), 
            self.to_align.getDocumentStats(), 
            self.alignment_matches
            )

        addHeader = False
        if not FileUtils.isFileExist(self.processing_stats_file):
            addHeader = True

        with open(self.processing_stats_file, 'a+',encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';', escapechar='/', quoting=csv.QUOTE_NONE)
            if addHeader:
                writer.writerow(stats.getHeaders())
            writer.writerow(stats.getValues())


       
    def getRogueScore(self, process, align):
        #todo
        return 0 


    def getBlueScore(self, process, align):
        #todo
        return 0 
    
    def getMereorScore(self, process, align):
        #todo
        return 0
