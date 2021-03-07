from abc import ABC, abstractmethod
from tools import ConfigUtils, ConfigConsts
from dataset import AbstractDataset, DatasetFactory
from alignment import AlignmentFactory, AbstractAlignment
from evaluation import EvaluationFactory, AbstractEvaluation
import numpy as np
import os
import datetime

class AbstractEngine(ABC):


    @abstractmethod
    def initialize(self, config_utils : ConfigUtils) -> None:
        pass


    @abstractmethod
    def doProcessing(self, uniqueProcessingId) -> None:
        pass


    def __init__(self):
        self.local_config_utils = None
        self.output_folder_for_process = None
        super().__init__()

    def getDataSet(self) -> AbstractDataset:
        dataset_type =  self.local_config_utils.getValue(ConfigConsts.CONF_SEC_DATASET,ConfigConsts.CONF_DATASET_TYPE)
        dataSet = DatasetFactory().getDataset(dataset_type, self.local_config_utils)
        assert dataSet, "DataSet unknow"
        return dataSet

    def getAlignmentType(self) -> AbstractAlignment:
        return AlignmentFactory().getAlignment(self.local_config_utils)

    def getUniqueProcessingId(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")

    def getEvaluation(self) -> list:
        return EvaluationFactory().getEvaluations(self.local_config_utils)

    def getStatistic(self, statistic_name, values):
        floatlist = np.array(values, np.float)
        meanscore = np.mean(floatlist)
        variance = np.var(floatlist)
        stdev = np.std(floatlist)
        total = len(values)
        out="Type: "+statistic_name + "\n"
        out+="The mean: %s" % meanscore + "\n"
        out+="The variance : %s" % variance + "\n"
        out+="The std: %s" % stdev + "\n"
        out+="The total: %s" % total + "\n"
        return out
    
    def scanResults(self, statistic_name):
        column_with_data = None
        values = []
        for file in os.listdir(self.output_folder_for_process):
            if file.endswith("_alignment.csv"):
                results = os.path.join(self.output_folder_for_process, file)
                with open(results) as f:
                    for index, line in enumerate(f):
                        separated = line.rstrip("\n").split(";")
                        if len(separated) > 1 and index ==0:
                            for index_of_column, column in enumerate(separated):
                                if column == statistic_name:
                                    column_with_data = index_of_column
                                    continue
                        elif len(separated) > 1 and index >0:
                            values.append(separated[column_with_data])
        outputGlobalStats = os.path.join(self.output_folder_for_process, 'processing_info.txt')
        with open(outputGlobalStats, 'w+') as f:
            f.write(self.getStatistic(statistic_name,values))

                                
                            




    def execute(self) -> None:
        processing_info = self.local_config_utils.getValue(ConfigConsts.CONF_SEC_ENGINE, ConfigConsts.CONF_ENGINE_PROCESSING_INFO)
        if self.local_config_utils.hasMultipleConfiguration():
            for conf_nbr in range(self.local_config_utils.getNumberOfConfiguration()):
                self.local_config_utils.setActiveConfiguration(conf_nbr)
                processing_info = self.local_config_utils.getValue(ConfigConsts.CONF_SEC_ENGINE, ConfigConsts.CONF_ENGINE_PROCESSING_INFO)
                self.doProcessing(self.getUniqueProcessingId())
                if processing_info == str(True) or processing_info == True:
                    self.scanResults('similarity')
        else:
            self.doProcessing(self.getUniqueProcessingId())
            if processing_info == str(True) or processing_info == True:
                    self.scanResults('similarity')

    