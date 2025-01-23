import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from app.preprocess import DocumentPreprocessor

class LocalSearch:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/msmarco-bert-base-dot-v5')
        self.dimension = 768
        self.index = faiss.IndexFlatIP(self.dimension)
        self.text_data = None

    def build_index(self, directory_path):
         # Preprocess the documents in the specified directory
        self.text_data = DocumentPreprocessor.preprocess_directory(directory_path)

        # Encode the documents into embeddings
        embeddings = np.array(self.model.encode(self.text_data))

        # Initialize the FAISS index with inner product (Euclidean distance)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)

        # Normalize embeddings
        faiss.normalize_L2(embeddings)

        # Add embeddings to the index
        self.index.add(embeddings)

    def search(self, query, top_k=5):
        if self.index is None:
            raise ValueError("Index not built. Call `build_index` first.")
        # Generate the query embedding
        query_embedding = self.model.encode([query])[0]

        # Perform the FAISS search
        distances, indices = self.index.search(np.array([query_embedding]), top_k)

        # Gather results with metadata
        results = []
        for i, idx in enumerate(indices[0]):
            result_data = {
                "id": int(idx),
                "content": self.text_data[idx],
                "score": float(distances[0][i]),
            }
            print(f"ID: {idx}, Score: {float(distances[0][i])}")
            results.append(result_data)

        print(f"Found {len(results)} results for the query: '{query}'")
        return results
