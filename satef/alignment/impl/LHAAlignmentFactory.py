from alignment import AbstractAlignmentFactory
from alignment import AbstractAlignment
from alignment.impl import LHAAlignment

class LHAAlignmentFactory(AbstractAlignmentFactory):
 
    def getAlignment(self) -> AbstractAlignment:
        return LHAAlignment()
    