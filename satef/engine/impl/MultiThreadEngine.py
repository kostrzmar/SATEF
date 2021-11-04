from engine import AbstractEngine
from alignment import AbstractAlignment
from tools import ConfigUtils, ConfigConsts, FileUtils
from tqdm import tqdm
from multiprocessing import Process, Manager, cpu_count
import logging

class MultiThreadEngine(AbstractEngine):
    

    def initialize(self, config_utils : ConfigUtils) -> None:
        self.local_config_utils = config_utils
        logging.info("Multi Thread Engine initialization done")
    
    def doProcessing(self, uniqueProcessingId) -> None:
        data_set = self.getDataSet()
        pbar = tqdm(total=data_set.getTotalFiles(), desc="Progress")
        is_processing_done = False
        self.is_reverse_processing = data_set.is_reverse
        evaluationMetrics = self.getEvaluation()
        num_workers=int(self.local_config_utils.getValue(ConfigConsts.CONF_SEC_ENGINE, ConfigConsts.CONF_ENGINE_EXECUTE_PARALLER_NBR_OF_PROCESSES))
        logging.info("Parallel processing with [{}] processes".format(num_workers))
        while not is_processing_done:
            pool = []
            for _ in range(num_workers):
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
                        p = Process(target=alignment_type.doAlignment, args=())
                        pool.append(p)
                        p.start()

            for p in pool:
                p.join()
                pbar.update()
                
        pbar.close()
        logging.info("Multi Thread Engine do processing done")
    

        