import os
import logging
from configparser import ConfigParser, ExtendedInterpolation
import yaml
import pathlib


class ConfigUtils():

    def __init__(self, pathToConfiguration):        
        assert pathToConfiguration, "Configuration can't be found"
        suffix = pathlib.Path(pathToConfiguration).suffix
        self.config_as_dict = None
        self.multiple_config = None
        if suffix == '.init':
            self.config_as_dict = self.loadConfigParser(pathToConfiguration)    
        elif suffix =='.yaml':
            self.config_as_dict = self.loadYaml(pathToConfiguration)        
        assert self.config_as_dict, "Configuration initialization failed"
        super().__init__() 

    def extractDataFromConfig(self, configParser: ConfigParser, sectionName):
        section_as_dict = {}
        options = configParser.options(sectionName)
        for option in options:
            section_as_dict[option]  = configParser.get(sectionName,option)
        return section_as_dict


    def loadConfigParser(self, pathToConfiguration):
        config_as_dict = {}
        config_parser =  ConfigParser(interpolation=ExtendedInterpolation())
        if not config_parser.read(pathToConfiguration):
                logging.error("Config file [{}] not found".format(pathToConfiguration))
                raise FileNotFoundError(pathToConfiguration) 
        sections = config_parser.sections()
        for section in sections:
            config_as_dict[section]=self.extractDataFromConfig(config_parser, section)

        defaults = config_parser.defaults()
        default_dict = {}
        for key in defaults:
            default_dict[key] = defaults[key]
        config_as_dict["default_section"] = default_dict
        return config_as_dict
    
    def loadYaml(self, pathToConfiguration):
        multiple_config = []
        try:
            with open(pathToConfiguration, "r") as fh:
                multiple_config = list(yaml.load_all(fh, Loader=yaml.SafeLoader))
        except yaml.YAMLError as exc:
            return exc
        self.multiple_config = multiple_config
        return self.multiple_config[0]

    def getValue(self, sectionName, propertyName, defaultValue=None):
        if propertyName in self.config_as_dict[sectionName]:
            return self.config_as_dict[sectionName][propertyName]
        else:
            return defaultValue  
    
    def hasMultipleConfiguration(self):
        return self.multiple_config and len(self.multiple_config)>1

    def getNumberOfConfiguration(self):
        return len(self.multiple_config)

    def setActiveConfiguration(self, index):
        assert index < self.getNumberOfConfiguration(), "No configuration for the index->"+str(index)
        self.config_as_dict = self.multiple_config[index]
