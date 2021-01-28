from sentence_transformers import SentenceTransformer
from tools import SingletonMeta

class TransformerEmbedder(metaclass=SingletonMeta):

    embedder = None

    def __init__(self, model) -> None:
        self.embedder = SentenceTransformer(model)