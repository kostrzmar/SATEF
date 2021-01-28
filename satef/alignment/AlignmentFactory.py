from alignment import AbstractAlignment
from alignment.impl import NaiveAlignmentFactory, MASSAlignAlignmentFactory, LHAAlignmentFactory, TransformerAlignmentFactory
from tools import ConfigConsts
from alignment import AbstractAlignmentFactory

class AlignmentFactory:

    def getAlignment(self, config_utils : ConfigConsts) -> AbstractAlignment:
        assert config_utils ,"Configuration is empty"
        aligmentType = config_utils.getValue(ConfigConsts.CONF_SEC_ALIGNMENT, ConfigConsts.CONF_ALIGNMENT_TYPE)
        alignment_factory = None 
        if aligmentType == ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_NAIVE:
            alignment_factory = NaiveAlignmentFactory()
        elif aligmentType == ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_MASSALIGN:
            alignment_factory = MASSAlignAlignmentFactory()
        elif aligmentType == ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_LHA:
            alignment_factory = LHAAlignmentFactory()
        elif aligmentType == ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_TRANSFORMER:
            alignment_factory = TransformerAlignmentFactory()    
        assert alignment_factory, "Alignment Factory unknow"
        alignment_job = alignment_factory.getAlignment()
        
        return alignment_job 

"""
    def getAlignment(self, alignmentType, config_parser, to_process, to_align, direction_prefix, unique_processing_stats_file_name):
        if alignmentType == "LHA":
            return LHAAlignment(config_parser, to_process, to_align, direction_prefix, unique_processing_stats_file_name)
        if alignmentType == "TRANSFORMER":
            
            return TransformerAlignment(config_parser, to_process, to_align, direction_prefix, unique_processing_stats_file_name)
            "" "
            transformerEmbedder = TransformerEmbedder(config_parser[consts.CONF_SEC_ALIGNMENT_TOOL][consts.CONF_ALIGNMENT_TOOL_TYPE_TRANSFORMER_MODEL])
            return TransformerAlignment(config_parser, to_process, to_align, direction_prefix, unique_processing_stats_file_name, embedder=transformerEmbedder)
            "" "
        if alignmentType == "NAIVE":
            return NaiveAlignment(config_parser, to_process, to_align, direction_prefix, unique_processing_stats_file_name)
        if alignmentType == 'MASSALIGN':
            return MASSAlignAlignment(config_parser, to_process, to_align, direction_prefix, unique_processing_stats_file_name)
        return None 

"""