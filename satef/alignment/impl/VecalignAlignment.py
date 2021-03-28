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

    def getOverLapCommand(self, fileName, overlapNbr):
        return 'python "'+self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_PATH)+'/overlap.py" -i "{}" -o "{}.overlap" -n {}'.format(fileName, fileName, overlapNbr)

    def getLaserEmbedingCommand(self, fileName, language):
        FileUtils.removeIfExit(fileName+".overlap.emb")
        #return self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_LASER_PATH)+'/tasks/embed/embed.sh {}.overlap {} {}.overlap.emb'.format(fileName, language, fileName)
        return '$LASER/tasks/embed/embed.sh {}.overlap {} {}.overlap.emb'.format(fileName, language, fileName)


    def getAlignCommand(self, orginal, target, overlapNbr):
        scr_overlaps = orginal+".overlap"
        trg_overlaps = target+".overlap"
        return 'python "'+self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_PATH)+'/vecalign.py" --alignment_max_size '+str(overlapNbr)+' --src "{}" --tgt "{}" --src_embed "{}" "{}"  --tgt_embed "{}" "{}" '.format(orginal, target, scr_overlaps, scr_overlaps+".emb", trg_overlaps, trg_overlaps+".emb")

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
        overlapNbr = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_MAX_SIZE)
        language = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_LANGUAGE)
        os.system(self.getOverLapCommand(self.to_process.path_to_document, overlapNbr))
        os.system(self.getOverLapCommand(self.to_align.path_to_document, overlapNbr))
        os.putenv('LASER', self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_VECALIGN_LASER_PATH))
        os.system(self.getLaserEmbedingCommand(self.to_process.path_to_document, language))
        os.system(self.getLaserEmbedingCommand(self.to_align.path_to_document, language))
        output = subprocess.check_output( self.getAlignCommand(self.to_process.path_to_document, self.to_align.path_to_document, overlapNbr), shell=True)
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

