from dataset.impl import DefaultDataset, SimpleComplexPairDataset, WikipediaDataset


class DatasetFactory:
    def getDataset(self, datasetType, configParser):
        if datasetType == "DEFAULT":
            return DefaultDataset(configParser)
        elif datasetType == "SIMPLE_COMPLEX_PAIR":
            return SimpleComplexPairDataset(configParser)
        elif datasetType == "WIKIPEDIA":
            return WikipediaDataset(configParser)
        return None 