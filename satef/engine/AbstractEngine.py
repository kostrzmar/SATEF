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
        self.is_reverse_processing = False
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

    def convertGold(self, fileEndingName):
        gold = {}
        input_folder  = self.local_config_utils.getValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_PATH)
        for file in os.listdir(input_folder):
            if file.endswith(fileEndingName):
                out = []
                results = os.path.join(input_folder, file)
                file_prefix = file.split(".")[0]
                with open(results) as f:
                    for index, line in enumerate(f):                
                        separated = line.rstrip("\n").split(";")
                        simple_id = separated[0] 
                        original_id = separated[1] 
                        out.append([simple_id, original_id])
                gold[file_prefix]=out
        return gold


    def getGold(self):
        gold = self.convertGold(".gold.txt")
        gold_partial=self.convertGold(".gold.partial.txt")
        return gold, gold_partial

    def getPrediction(self, fileName):
        prediction = []
        with open(fileName) as f:
            skip_header = True
            for index, line in enumerate(f):                
                separated = line.rstrip("\n").split(";")
                if skip_header:
                    skip_header = False
                else:
                    org_id = separated[1] #orginal
                    trg_id = separated[2] #simple
                    prediction.append([trg_id,org_id])
        return prediction

    def intrinsic_valuation(self, predict, gold):
        _recall = 0
        _precision = 0
        _f1 = 0
        _aer = 0
        count = 0
        for item in predict:
            if item in gold: 
                count +=1
        if len(predict) > 0:
            _precision = count / len(predict)
        if len(gold) >0:
            _recall = count / len(gold)
        if _precision+_recall>0:    
            _f1 = (2*_precision*_recall)/(_precision+_recall)
        if len(predict) + len(gold) > 0:
            _aer = 1 - ((2*count)/(len(predict)+len(gold)))
        return _precision, _recall, _f1, _aer

    def convertToTable(self, goldItems):
        out = []
        for key in goldItems:
            for items in goldItems[key]:
                out.append([key+"_"+str(items[0]), key+"_"+str(items[1])])   
        return out


    def evaluateWithGoldStandard(self):
        predicted_alignments = {}
        gold_alignments, gold_alignments_partial = self.getGold()
        for file in os.listdir(self.output_folder_for_process):
            if file.endswith("_alignment.csv"):
                results = os.path.join(self.output_folder_for_process, file)
                file_prefix = file.split("_vs_")[0].split(".")[0]

                prediction = self.getPrediction(results)
                predicted_alignments[file_prefix] = prediction
        
        gold = self.convertToTable(gold_alignments)
        gold_partials = self.convertToTable(gold_alignments_partial)
        pred = self.convertToTable(predicted_alignments)
        gold_stadart_evaluation = self.local_config_utils.getValue(ConfigConsts.CONF_SEC_ENGINE, ConfigConsts.CONF_ENGINE_EXECUTE_GOLD_EVALUATION)
        gold_standart_evaluation_combinded =self.local_config_utils.getValue(ConfigConsts.CONF_SEC_ENGINE, ConfigConsts.CONF_ENGINE_EXECUTE_GOLD_EVALUATION_COMBINE_SURE_POSSIBLE)
        precision, recall, f1, aer =0,0,0,0
        if gold_stadart_evaluation =="SURE":
            if  gold_standart_evaluation_combinded == str(True) or gold_standart_evaluation_combinded==True:
                precision, recall, f1, aer =self.intrinsic_valuation(pred, gold+gold_partials)
            else:
                precision, recall, f1, aer =self.intrinsic_valuation(pred, gold)
        else:
            precision, recall, f1, aer =self.intrinsic_valuation_sure_possible(pred, gold, gold_partials)
        
        outputGlobalStats = os.path.join(self.output_folder_for_process, 'evaluation.txt')
        with open(outputGlobalStats, 'w+') as f:
            f.write('Total documents [{}] -> precision: {:.2f}  recall: {:.2f}  f1: {:.2f} aer: {:.2f}'.format(len(gold_alignments), precision, recall, f1, aer))
        
    
        newItem = []
        both = gold+gold_partials
        for item in pred:
            if item not in both:
                newItem.append(item)

        out = self.prepareToExtractSentence(gold+gold_partials+newItem)
        simple, normal = self.getSentenceBasedOnIndex(out)         


        countGold=0
        foundInGold=0
        row='Gold standard evaluation [{}] using combine gold+partial [{}] \n'.format(gold_stadart_evaluation, gold_standart_evaluation_combinded)
        row+='Total documents [{}] -> precision: {:.2f}  recall: {:.2f}  f1: {:.2f} aer: {:.2f}\n'.format(len(gold_alignments), precision, recall, f1, aer)
        row+="\n"
        row+="------GOLD------\n"
        used = []
        for item in gold:
            countGold+=1 
            row_1 = item[0]+";"+item[1]
            if item in pred:
                row_1+=";Found"
                foundInGold+=1
                used.append(item)
            else:
                row_1+=";Not_Found"               
            row+=row_1+"\n"
            row+=simple[item[0]].rstrip()+"\n"
            row+=normal[item[1]].rstrip()+"\n"
            row+="\n"
        row+="\n"
        row+='Total gold [{}] found in gold [{}] i.e. [{:.2f}%]'.format(countGold, foundInGold, (foundInGold/countGold)*100)
        row+="\n\n"
        row+="------PARTIAL------\n"
        countPartial=0
        foundInPartial=0
        for item in gold_partials: 
            countPartial+=1
            row_1 = item[0]+";"+item[1]
            if item in pred:
                row_1+=";Found"
                foundInPartial+=1
                used.append(item)
            else:
                row_1+=";Not_Found" 
            row+=row_1+"\n"
            row+=simple[item[0]].rstrip()+"\n"
            row+=normal[item[1]].rstrip()+"\n"
            row+="\n"
        row+="\n"
        row+='Total partial [{}] found in partial [{}] i.e. [{:.2f}%]'.format(countPartial, foundInPartial, (foundInPartial/countPartial)*100)
        row+="\n\n"
        row+="------NEW------\n"
        newPrediction=0
        for item in pred: 
            if item not in used:
                newPrediction+=1
                row+=item[0]+";"+item[1]+"\n"
                row+=simple[item[0]].rstrip()+"\n"
                row+=normal[item[1]].rstrip()+"\n"
                row+="\n"
        row+="\n"
        row+='Total new [{}] of [{}]  i.e. [{:.2f}%]'.format(newPrediction, len(pred),  (newPrediction/len(pred))*100)
        row+="\n"

        outputEvaluationDetails = os.path.join(self.output_folder_for_process, 'evaluation_details.txt')        
        with open(outputEvaluationDetails, 'w+') as f:
            f.write(row)     


                            
    def intrinsic_valuation_sure_possible(self, predict, goldSure, goldPossible):
        countP = 0
        countS = 0
        for item in predict:
            if item in goldSure: 
                countS +=1
            if item in goldPossible:
                countP +=1
        _precision = countP / len(goldPossible)
        _recall = countS / len(goldSure)
        _aer = 1 - ((countS + countP)/(len(goldSure)+len(predict)))
        return _precision, _recall, 1-_aer, _aer  

    def prepareToExtractSentence(self, data):
        out = {}
        simple_ids, normal_ids =[],[]
        for item in data:
            file_name = item[0][ : item[0].rfind("_")]
            simple = item[0].split("_")[-1]
            normal = item[1].split("_")[-1]
            if file_name not in out:
                out[file_name] = []
            out[file_name].append([simple, normal])
        return out



    def getSentenceBasedOnIndex(self, data):
        simple = {}
        normal = {}
        for file_name in data:  
            input_folder  = self.local_config_utils.getValue(ConfigConsts.CONF_SEC_DATASET, ConfigConsts.CONF_DATASET_PATH)
            simple_file = os.path.join(input_folder, file_name+".simple.txt")
            normal_file = os.path.join(input_folder, file_name+".normal.txt")
            index_simple = []
            index_normal = []
            for item in data[file_name]:
                index_simple.append(item[0])
                index_normal.append(item[1])
            with open(simple_file) as f:
                for index, line in enumerate(f):   
                    if str(index) in index_simple:
                        simple[file_name+"_"+str(index)] = line
            with open(normal_file) as f:
                for index, line in enumerate(f):   
                    if str(index) in index_normal:
                        normal[file_name+"_"+str(index)] = line
        return simple, normal 


    def execute(self) -> None:
        processing_info = self.local_config_utils.getValue(ConfigConsts.CONF_SEC_ENGINE, ConfigConsts.CONF_ENGINE_PROCESSING_INFO)
        gold_standard = self.local_config_utils.getValue(ConfigConsts.CONF_SEC_ENGINE, ConfigConsts.CONF_ENGINE_EXECUTE_GOLD_STANDART)
        if self.local_config_utils.hasMultipleConfiguration():
            for conf_nbr in range(self.local_config_utils.getNumberOfConfiguration()):
                self.local_config_utils.setActiveConfiguration(conf_nbr)
                processing_info = self.local_config_utils.getValue(ConfigConsts.CONF_SEC_ENGINE, ConfigConsts.CONF_ENGINE_PROCESSING_INFO)
                self.doProcessing(self.getUniqueProcessingId())
                if processing_info == str(True) or processing_info == True:
                    self.scanResults('similarity')
                if gold_standard == str(True) or processing_info == True:
                    self.evaluateWithGoldStandard()
        else:
            self.doProcessing(self.getUniqueProcessingId())
            if processing_info == str(True) or processing_info == True:
                self.scanResults('similarity')
            if gold_standard == str(True) or processing_info == True:
                self.evaluateWithGoldStandard()


    