from alignment import AbstractAlignment
from alignment.impl import NaiveAlignmentFactory, MASSAlignAlignmentFactory, LHAAlignmentFactory, TransformerAlignmentFactory, CATSAlignmentFactory, VecalignAlignmentFactory
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
        elif aligmentType == ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_CATS:
            alignment_factory = CATSAlignmentFactory()
        elif aligmentType == ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN:
            alignment_factory = VecalignAlignmentFactory()    
        assert alignment_factory, "Alignment Factory unknow"
        alignment_job = alignment_factory.getAlignment()
        
        return alignment_job 
