from alignment import AbstractAlignment
from alignment.data import AlignmentMatch
from document import TextDocument
from tools  import FileUtils
from tools import ConfigConsts
import os
from Utils import MyIOutils, TextProcessingUtils, DefinedConstants, VectorUtils
from Representations import ModelContainer, NgramModel, EmbeddingModel
import subprocess
output = subprocess.check_output("cat /etc/services", shell=True)


class VecalignAlignment(AbstractAlignment):

    def getToolId(self):
        return 60

    def getOutputPrefix(self):
        return "VECALIGN"

    def getAlignCommand(self, orginal, target):
        scr_overlaps = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_SRC_OVERLAPS_PATH)
        trg_overlaps = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_TRG_OVERLAPS_PATH)
        return 'python "'+self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_PATH)+'/vecalign.py" --alignment_max_size '+str(self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_MAX_SIZE))+' --src "{}" --tgt "{}" --src_embed "{}" "{}"  --tgt_embed "{}" "{}" '.format(orginal, target, scr_overlaps, scr_overlaps+".emb", trg_overlaps, trg_overlaps+".emb")

    def convertToInt(self, s):
        if s:
            return int(s)
        pass

    def textToList(self, toList):
        return list(map(self.convertToInt, toList.strip('[]').replace('\'', '').replace(' ', '').split(',')))

    def readFileToArray(self, file):
        out = []
        with open(file,"r") as f:
            for i in f.readlines():
                if not i.strip():
                    continue
                if i:
                    out.append(i.strip()) 
        return out 


    def concatenateString(self, textAsArray, listOfItem):
        out = ""
        for index  in range(len(listOfItem)):
            out += str(textAsArray[listOfItem[index]]).rstrip() + " "
        return out

    def align(self):
        FileUtils.removeIfExit(self.output_file)
        output = subprocess.check_output( self.getAlignCommand(self.to_process.path_to_document, self.to_align.path_to_document), shell=True)
        inpAsArray = self.readFileToArray(self.to_process.path_to_document)
        trgAsArray = self.readFileToArray(self.to_align.path_to_document)
        strVal = str(output, 'utf-8') 
        alignments = list(strVal.split("\n")) 
        for alingment in alignments:
            items = alingment.split(":")
            if len(items)>1: 
                srcList = self.textToList(items[0])
                trgList = self.textToList(items[1])

                if srcList[0] and trgList[0]:
                    match = self.getAligmentMatch()
                    match.process_line_id = str(srcList)
                    match.align_line_id = str(trgList)
                    match.process_line = self.cleanTest(self.concatenateString(inpAsArray, srcList).rstrip())
                    match.align_line = self.cleanTest(self.concatenateString(trgAsArray, trgList).rstrip())
                    match.similarity = items[2]
                    self.alignment_matches.append(match)

