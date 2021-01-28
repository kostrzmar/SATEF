from tools import ConfigUtils, ConfigConsts
from engine import AbstractEngine
from engine.impl import SingleThreadEngineFactory, MultiThreadEngineFactory
import logging
import transformers


class EngineFactory:
    def getEngine(self, configurationFile) -> AbstractEngine:

        transformers.tokenization_utils.logger.setLevel(logging.ERROR)
        transformers.configuration_utils.logger.setLevel(logging.ERROR)
        transformers.modeling_utils.logger.setLevel(logging.ERROR)
        assert configurationFile ,"Configuration is empty"

        config_utils = ConfigUtils(configurationFile)
        mode = config_utils.getValue(ConfigConsts.CONF_SEC_ENGINE, ConfigConsts.CONF_ENGINE_EXECUTE_PARALLER)
        engine_factory = None 
        if mode == str(False) or mode == False:
            engine_factory = SingleThreadEngineFactory()
        elif mode == str(True) or mode == True:
            engine_factory = MultiThreadEngineFactory()
        assert engine_factory, "Engine Factory unknow"
        engine_job = engine_factory.getEngine()
        engine_job.initialize(config_utils)
        return engine_job 