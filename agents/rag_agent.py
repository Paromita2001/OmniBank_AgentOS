import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder


INDEX_PATH = "services/vectorstore/rag/faiss_index.index"
META_PATH = "services/vectorstore/rag/faiss_meta.pkl"

# Embedding model (for FAISS retrieval)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Cross-encoder model (for re-ranking)
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


class RAGAgent:
    """
    RAG Agent with Cross-Encoder Re-Ranking
    """

    def __init__(self):
        self.index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def handle(self, *, query: str):

        # Step 1: Embed query for FAISS
        query_embedding = embed_model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        # Step 2: Retrieve top 5 candidates
        distances, indices = self.index.search(query_embedding, k=5)

        candidates = []
        for idx in indices[0]:
            question_text = self.metadata[idx]["question"]
            candidates.append((idx, question_text))

        if not candidates:
            return "Sorry, I could not find relevant information."

        # Step 3: Cross-Encoder re-ranking
        cross_inputs = [
            (query, candidate_question)
            for _, candidate_question in candidates
        ]

        scores = cross_encoder.predict(cross_inputs)

        # Step 4: Pick best score
        best_index = np.argmax(scores)
        best_score = scores[best_index]

        # Confidence threshold
        if best_score < 0.5:
            return "Sorry, I could not find relevant information."

        best_metadata_index = candidates[best_index][0]

        return self.metadata[best_metadata_index]["answer"]
