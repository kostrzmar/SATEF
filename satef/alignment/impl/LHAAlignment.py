from alignment import AbstractAlignment
from alignment.data import AlignmentMatch
from document import TextDocument
from tools  import FileUtils
from sentence_transformers import SentenceTransformer
import scipy.spatial
from tools import ConfigConsts
import os

class LHAAlignment(AbstractAlignment):

    def getToolId(self):
        return 30

    def getOutputPrefix(self):
        return "LHA"

    def getIndexCommand(self, file, model):
        return 'python "'+self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_LHA_PATH)+'/build_annoy_index.py" -src_file "{}" -emb sent2vec -vec_size 600 -model {}'.format(file, model)

    def getAlignCommand(self, orginal, target, model):
        return 'python "'+self.getConfigValue(self.getToolSecName(), ConfigConsts.CONF_ALIGNMENT_TOOL_TYPE_LHA_PATH)+'/aligner.py" -level hierarchical -src "{}" -tgt "{}" -emb sent2vec -vec_size 600 -batch_size 50 -lower_th 0.70 -k_best 2 -refine_all true -w2v {}'.format(orginal, target, model)

    def cleanUpUniqueKey(self, filename, newFileName):
        f = open(filename, "r")
        g = open(newFileName, "w")
        for line in f:
            if line.strip():
                g.write("".join(line.split(";")[-1]))


    def align(self):
        
        FileUtils.removeIfExit(self.output_file)
        model = 'wiki_de'
        post_fix = ".hier.None"
        post_fix_id = post_fix+".id"
        out_similarity = '.sims.None'
        orginal_Id = self.to_process.path_to_document+post_fix_id
        orginal_Text = self.to_process.path_to_document+post_fix
        simple_Id = self.to_align.path_to_document +post_fix_id
        simple_Text = self.to_align.path_to_document + post_fix
        similarity = self.to_process.path_to_document+"."+FileUtils.getFileFromPath(self.to_align.path_to_document)+out_similarity
        FileUtils.removeIfExit(orginal_Id)
        FileUtils.removeIfExit(orginal_Text)
        FileUtils.removeIfExit(simple_Id)
        FileUtils.removeIfExit(simple_Text)
        FileUtils.removeIfExit(similarity)


        os.system(self.getIndexCommand(self.to_process.path_to_document, model))
        os.system(self.getIndexCommand(self.to_align.path_to_document, model))
        os.system(self.getAlignCommand(self.to_process.path_to_document, self.to_align.path_to_document,model))


        with open(orginal_Id) as o_id, open(simple_Id) as s_id, open(similarity) as sim, open(orginal_Text, encoding='utf8') as o_T, open(simple_Text, encoding='utf8') as s_T:
            for line_o_id, line_s_id, line_sim, line_o_T, line_s_T in zip(o_id, s_id, sim, o_T, s_T):
                match = self.getAligmentMatch()
                match.process_line_id = line_o_id.rstrip()
                match.align_line_id = line_s_id.rstrip()
                match.process_line = self.cleanTest(line_o_T.rstrip())
                match.align_line = self.cleanTest(line_s_T.rstrip())
                match.similarity = line_sim.rstrip()
                self.alignment_matches.append(match)

        
                    
