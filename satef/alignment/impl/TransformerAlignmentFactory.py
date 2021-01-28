from alignment import AbstractAlignmentFactory
from alignment import AbstractAlignment
from alignment.impl import TransformerAlignment

class TransformerAlignmentFactory(AbstractAlignmentFactory):
 
    def getAlignment(self) -> AbstractAlignment:
        return TransformerAlignment()
    