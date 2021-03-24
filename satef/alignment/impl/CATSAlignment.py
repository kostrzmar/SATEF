from alignment import AbstractAlignment
from alignment.data import AlignmentMatch
from document import TextDocument
from tools  import FileUtils
from tools import ConfigConsts
import os
from Utils import MyIOutils, TextProcessingUtils, DefinedConstants, VectorUtils
from Representations import ModelContainer, NgramModel, EmbeddingModel


class CATSAlignment(AbstractAlignment):

    def getToolId(self):
        return 50

    def getOutputPrefix(self):
        return "CATS"

    def align(self):    
        FileUtils.removeIfExit(self.output_file)
        vocab = set()
        alignmentLevel = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_CATS_ALIGNMENT_LEVEL)
        #language = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_CATS_LANGUAGE)
        similarityStrategy = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_CATS_SIMILARITY_STRATEGY)
        alignmentStrategy = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_CATS_ALIGNMENT_STRATEGY)
        subLvAlignmentStrategy = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_CATS_ALIGNMENT_SUBLEVEL_STRATEGY)
        embeddingsFile = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_CATS_EMBEDDING)
        lineLevel = self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_CATS_ALIGNMENT_LINE_LEVEL)
        if len(similarityStrategy) == 3 and similarityStrategy[0]=='C' and similarityStrategy[-1]=='G':
            nGramSize = int(similarityStrategy[1])
            similarityStrategy = DefinedConstants.CNGstrategy
            model = None 
        if similarityStrategy == DefinedConstants.CWASAstrategy or similarityStrategy==DefinedConstants.WAVGstrategy:            
            text = MyIOutils.readTextFile(self.to_process.path_to_document)
            vocab.update(TextProcessingUtils.getCleanEmbeddingModelTokens(text))
            text = MyIOutils.readTextFile(self.to_align.path_to_document)
            vocab.update(TextProcessingUtils.getCleanEmbeddingModelTokens(text))

            aux = EmbeddingModel(embeddingsFile, vocab)
            model = ModelContainer(aux, None)
            if similarityStrategy == DefinedConstants.CWASAstrategy:
                model.em.precomputeW2VcosDist()
                model.em.createSimilarityMatrix()
                
        elif similarityStrategy == DefinedConstants.CNGstrategy:
            aux = NgramModel(True, nGramSize)
            model = ModelContainer(None, aux)
            text = MyIOutils.readTextFile(self.to_process.path_to_document)
            aux.processAndCountTextNgrams(text, alignmentLevel)
            text = MyIOutils.readTextFile(self.to_align.path_to_document)
            aux.processAndCountTextNgrams(text, alignmentLevel)
            aux.calculateIDF()
        text1 = MyIOutils.readTextFile(self.to_process.path_to_document)
        cleanSubtexts1 = TextProcessingUtils.getCleanText(text1, alignmentLevel, similarityStrategy, model, lineLevel)
        text2 = MyIOutils.readTextFile(self.to_align.path_to_document)
        cleanSubtexts2 = TextProcessingUtils.getCleanText(text2, alignmentLevel, similarityStrategy, model, lineLevel)
        alignments = VectorUtils.alignUsingStrategy(cleanSubtexts1,	cleanSubtexts2, similarityStrategy, alignmentStrategy, model)
        if  alignmentLevel == DefinedConstants.ParagraphSepEmptyLineAndSentenceLevel:
            alignments = VectorUtils.getSubLevelAlignments(alignments, cleanSubtexts1, cleanSubtexts2, similarityStrategy, subLvAlignmentStrategy, model)
        for alingment in alignments:
            match = self.getAligmentMatch()
            match.process_line_id = alingment.index1
            match.align_line_id = alingment.index2
            match.process_line = self.cleanTest(str(alingment.source).rstrip())
            match.align_line = self.cleanTest(str(alingment.target).rstrip())
            match.similarity = alingment.similarity
            self.alignment_matches.append(match)


                    
