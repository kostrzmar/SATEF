from dataset import AbstractDataset
from tools import ConfigUtils,ConfigConsts, FileUtils
import datetime
import os
import logging

class SimpleComplexPairDataset(AbstractDataset):
    def __init__(self,  configParser : ConfigUtils):
        super().__init__(configParser)
        self.dataset_name = "SIMPLE_COMPLEX_PAIR"

    def getUniqueName(self):
        uniqeFileName = str(datetime.datetime.now().date())+"_"+str(datetime.datetime.now().time()).replace(':', '_')
        return  "stats_out_"+self.getDirectionPrefix()+"_"+uniqeFileName+".csv"

    def getInputFile(self):
        return self.getConfigValue(ConfigConsts.CONF_SEC_DATASET,ConfigConsts.CONF_DATASET_PATH)

    def getFiles(self):
        filesInFolder = os.listdir(self.input_folder)
        for file in filesInFolder:
            self.isReverse = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET,ConfigConsts.CONF_DATASET_ALIGNMENT_REVERSE)
            fileMasksToProcess = []
            if self.isReverse or eval(str(self.isReverse)):
                fileMaskReverseToProcess = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_PARAPHRASE_MASK)
                if fileMaskReverseToProcess.find(',')!=-1:
                    fileMasksToProcess = fileMaskReverseToProcess.split(",")   
                else:
                    fileMasksToProcess.append(fileMaskReverseToProcess)
            else:
                fileMasksToProcess.append(self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_ORIGINAL_MASK))
            for fileMaskToProcess in fileMasksToProcess:
                if file.endswith(fileMaskToProcess.strip()):
                    self.files.append(file)

    def getDirectionPrefix(self):
        self.isReverse = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET,ConfigConsts.CONF_DATASET_ALIGNMENT_REVERSE)
        if self.isReverse or eval(str(self.isReverse)):
            return self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_PARAPHRASE_MASK_PREFIX) + "-"+ self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_ORIGINAL_MASK_PREFIX)
        else:
            return self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_ORIGINAL_MASK_PREFIX)+ "-"+self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_PARAPHRASE_MASK_PREFIX) 

    def getRespectiveDocumentToCompare(self, fileName):
        if fileName:
            #isReverse = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET,ConfigConsts.CONF_DATASET_ALIGNMENT_REVERSE)
            orginDocument = None
            targetDocument = None
            if self.isReverse or eval(str(self.isReverse)):
                orginDocument = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_PARAPHRASE_MASK)
                targetDocument = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_ORIGINAL_MASK)
            else:
                orginDocument = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_ORIGINAL_MASK)
                targetDocument = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_PARAPHRASE_MASK)          
            respectiveDocumentName = fileName.replace(orginDocument,targetDocument)
            return FileUtils.getFullPath(self.input_folder, respectiveDocumentName)
        else:
            return None

    def getNextDocumentToProcess(self):   
        file = None
        if len(self.files) > self.current_file:
            file = self.files[self.current_file]
            self.current_file+=1

        if file:
            return FileUtils.getFullPath(self.input_folder, file)
        else:
            return None
