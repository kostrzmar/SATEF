from abc import ABC, abstractmethod
from tools import ConfigUtils
import os

class AbstractDataset(ABC):
    """ Abstract document class """

    def __init__(self, config_utils : ConfigUtils):
        self.dataset_name = "N/A"
        self.local_config_utils = config_utils
        self.input_folder = self.getInputFile()
        self.files = []
        self.files.append(self.getFiles())
        self.current_file = 0
        self.is_reverse = False

        super().__init__()

    def getFiles(self):
        return os.listdir(self.input_folder)

    def getTotalFiles(self):
        return len(self.files)
    
    def getConfigValue(self, section, key):
        return self.local_config_utils.getValue(section,key)

    @abstractmethod
    def getInputFile(self):
        pass

    @abstractmethod
    def getNextDocumentToProcess(self):
        pass

    @abstractmethod
    def getRespectiveDocumentToCompare(self, fileName):
        pass

    @abstractmethod
    def getDirectionPrefix(self):
        pass
    