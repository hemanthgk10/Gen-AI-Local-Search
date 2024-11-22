import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from app.preprocess import DocumentPreprocessor

class LocalSearch:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.text_data = None

    def build_index(self, directory_path):
        self.text_data = DocumentPreprocessor.preprocess_directory(directory_path)
        embeddings = np.array(self.model.encode(self.text_data))
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query, top_k=5):
        if self.index is None:
            raise ValueError("Index not built. Call `build_index` first.")
        query_embedding = np.array(self.model.encode([query]))
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.text_data[i] for i in indices[0]]
