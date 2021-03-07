from alignment import AbstractAlignmentFactory
from alignment import AbstractAlignment
from alignment.impl import VecalignAlignment

class VecalignAlignmentFactory(AbstractAlignmentFactory):
 
    def getAlignment(self) -> AbstractAlignment:
        return VecalignAlignment()
    