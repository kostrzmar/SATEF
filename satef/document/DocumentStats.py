class DocumentStats():
        
    def __init__(self):
        self.nbr_sentences = 0
        self.nbr_paragraphs =0 
        self.nbr_words = 0
        self.nbr_characters = 0
        super().__init__()

    def disply(self):
        print ("The number of sentences =", self.nbr_sentences)
        print ("The number of patagraphs =", self.nbr_paragraphs)
        print ("The number of words =",  self.nbr_words)
        print ("The number of characters =", self.nbr_characters)
 