from alignment import AbstractAlignmentFactory
from alignment import AbstractAlignment
from alignment.impl import NaiveAlignment

class NaiveAlignmentFactory(AbstractAlignmentFactory):
 
    def getAlignment(self) -> AbstractAlignment:
        return NaiveAlignment()
    