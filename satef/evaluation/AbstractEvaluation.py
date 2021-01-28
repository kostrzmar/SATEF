from abc import ABC, abstractmethod
from alignment.data import AlignmentMatch
from tools import ConfigUtils


class AbstractEvaluation(ABC):

    def __init__(self):
        self.metric_name = self.getMetricName()
        self.local_config_utils = None
        super().__init__()

    @abstractmethod
    def getMetricName(self):
        pass

    @abstractmethod
    def evaluate(self, alignmentMatches):
        pass
    
    def setConfigUtils(self, config_utils : ConfigUtils):
        self.local_config_utils = config_utils
