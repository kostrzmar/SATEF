from dataset import AbstractDataset
from tools import FileUtils
from tools import ConfigConsts
import os
import logging

class DefaultDataset(AbstractDataset):
    def __init__(self,  configParser):
        super().__init__(configParser)
        self.dataset_name = "DEFAULT"


    def getInputFile(self):
        return self.getConfigValue(ConfigConsts.CONF_SEC_DATASET,ConfigConsts.CONF_DATASET_INPUT_FOLDER)

    def getFiles(self):
        filesInFolder = os.listdir(self.input_folder)
        for file in filesInFolder:
            isReverse = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET,ConfigConsts.CONF_DATASET_ALIGNMENT_REVERSE)
            fileMasksToProcess = []
            if eval(isReverse):
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
        isReverse = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET,ConfigConsts.CONF_DATASET_ALIGNMENT_REVERSE)
        if  eval(isReverse):
            return self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_PARAPHRASE_MASK_PREFIX) + "-"+ self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_ORIGINAL_MASK_PREFIX)
        else:
            return self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_ORIGINAL_MASK_PREFIX)+ "-"+self.getConfigValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_PARAPHRASE_MASK_PREFIX) 

    def getRespectiveDocumentToCompare(self, fileName):
        if fileName:
            isReverse = self.getConfigValue(ConfigConsts.CONF_SEC_DATASET,ConfigConsts.CONF_DATASET_ALIGNMENT_REVERSE)
            orginDocument = None
            targetDocument = None
            if  eval(isReverse):
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
