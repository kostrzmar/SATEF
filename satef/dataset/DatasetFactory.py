from dataset.impl import DefaultDataset, SimpleComplexPairDataset

class DatasetFactory:
    def getDataset(self, datasetType, configParser):
        if datasetType == "DEFAULT":
            return DefaultDataset(configParser)
        elif datasetType == "SIMPLE_COMPLEX_PAIR":
            return SimpleComplexPairDataset(configParser)
        return None 