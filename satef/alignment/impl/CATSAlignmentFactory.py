from alignment import AbstractAlignmentFactory
from alignment import AbstractAlignment
from alignment.impl import CATSAlignment

class CATSAlignmentFactory(AbstractAlignmentFactory):
 
    def getAlignment(self) -> AbstractAlignment:
        return CATSAlignment()
    