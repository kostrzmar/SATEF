from engine import AbstractEngine
from alignment import AbstractAlignment
from tools import ConfigUtils, ConfigConsts, FileUtils
from tqdm import tqdm
import logging

class SingleThreadEngine(AbstractEngine):
    

    def initialize(self, config_utils : ConfigUtils) -> None:
        self.local_config_utils = config_utils
        logging.info("Single Thread Engine initialization done")
    
    def doProcessing(self, uniqueProcessingId) -> None:
        data_set = self.getDataSet()
        pbar = tqdm(total=data_set.getTotalFiles(), desc="Progress")
        self.is_reverse_processing = data_set.is_reverse
        is_processing_done = False
        evaluationMetrics = self.getEvaluation()
        while not is_processing_done:
            file_to_process = data_set.getNextDocumentToProcess()
            file_to_align = data_set.getRespectiveDocumentToCompare(file_to_process)
            if not file_to_process:
                is_processing_done = True
            else:
                if file_to_align and  FileUtils.isFileExist(file_to_align):
                    alignment_type = self.getAlignmentType()
                    alignment_type.initialize(
                        self.local_config_utils, 
                        file_to_process,
                        file_to_align,
                        data_set.getDirectionPrefix(),
                        uniqueProcessingId, 
                        evaluationMetrics
                    )
                    self.output_folder_for_process = alignment_type.getOutputDirectory()     
                    alignment_type.doAlignment()
            pbar.update()
            

        pbar.close()
        logging.info("Single Thread Engine do processing done")
    

        