from alignment import AbstractAlignmentFactory
from alignment import AbstractAlignment
from alignment.impl import MASSAlignAlignment

class MASSAlignAlignmentFactory(AbstractAlignmentFactory):
 
    def getAlignment(self) -> AbstractAlignment:
        return MASSAlignAlignment()
    