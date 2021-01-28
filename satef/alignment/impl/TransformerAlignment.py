from alignment import AbstractAlignment  
from alignment.data import AlignmentMatch
from alignment.impl import TransformerEmbedder
from document import TextDocument
from tools import FileUtils
from sentence_transformers import SentenceTransformer
import scipy.spatial
from tools import ConfigConsts

class TransformerAlignment(AbstractAlignment):

    def getToolId(self):
        return 40

    def getOutputPrefix(self):
        return "TRANSFORMER"

    def readFileToArray(self, file):
        out = []
        with open(file,"r") as f:
            for i in f.readlines():
                if not i.strip():
                    continue
                if i:
                    out.append(i.strip()) 
        return out 

    def align(self):
        FileUtils.removeIfExit(self.output_file)

        to_process = self.readFileToArray(self.to_process.path_to_document)
        to_align = self.readFileToArray(self.to_align.path_to_document)
	
        to_process_no_key = []
        to_align_no_key = []

        to_process_no_key = to_process.copy()
        to_align_no_key = to_align.copy()
            
        transformerEmbedder = TransformerEmbedder(self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_TRANSFORMER_MODEL))
        """
        transformerEmbedder = self.key_word_argument.get('embedder', None)
        """

        targetEmbeddings  = transformerEmbedder.embedder.encode(to_align_no_key, show_progress_bar=False)
        sourceEmbedding = transformerEmbedder.embedder.encode(to_process_no_key, show_progress_bar=False)
        closest_n = 1
        min_similarity = float( self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_TRANSFORMER_MIN_SIMILARITY))
        
        queryNbr = 0
        for query, query_embedding in zip(to_process, sourceEmbedding):
            distances = scipy.spatial.distance.cdist([query_embedding], targetEmbeddings, "cosine")[0]
            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])
            for idx, distance in results[0:closest_n]:
                if(1-distance > min_similarity):
                    match = self.getAligmentMatch()
                    match.process_line_id = queryNbr
                    match.align_line_id = idx
                    match.process_line = self.cleanTest(query.strip().rstrip())
                    match.align_line = self.cleanTest(to_align[idx].strip().rstrip())
                    match.similarity = 1-distance
                    match.blue_score = self.getBlueScore(match.process_line, match.align_line)
                    match.meteor_score = self.getMereorScore(match.process_line, match.align_line)
                    self.alignment_matches.append(match)
            queryNbr+=1

        
                    
                    
                   
                  
        
