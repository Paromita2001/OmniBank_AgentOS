import os
import re
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


DATA_FOLDER = "data/rag"
INDEX_PATH = "services/vectorstore/rag/faiss_index.index"
META_PATH = "services/vectorstore/rag/faiss_meta.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")


def parse_qa_file(filepath):
    """
    Parse Q&A formatted TXT file safely.
    """

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(filepath, "r", encoding="latin-1") as f:
            text = f.read()

    qa_pairs = []

    pattern = r"Q:(.*?)A:(.*?)(?=Q:|$)"
    matches = re.findall(pattern, text, re.DOTALL)

    for q, a in matches:
        qa_pairs.append({
            "question": q.strip(),
            "answer": a.strip()
        })

    return qa_pairs



# def build_faiss_index():
#     """
#     Build FAISS index from all TXT Q&A files.
#     Run this once.
#     """
#     all_data = []

#     for file in os.listdir(DATA_FOLDER):
#         if file.endswith(".txt"):
#             path = os.path.join(DATA_FOLDER, file)
#             all_data.extend(parse_qa_file(path))

#     questions = [item["question"] for item in all_data]

#     embeddings = model.encode(questions)
#     embeddings = np.array(embeddings).astype("float32")

#     dim = embeddings.shape[1]
#     index = faiss.IndexFlatL2(dim)
#     index.add(embeddings)

#     # Save index
#     faiss.write_index(index, INDEX_PATH)

#     # Save metadata
#     with open(META_PATH, "wb") as f:
#         pickle.dump(all_data, f)

#     print("FAISS index built successfully.")




def build_faiss_index():
    """
    Build FAISS index from all TXT Q&A files.
    Run this once.
    """
    all_data = []

    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".txt"):
            path = os.path.join(DATA_FOLDER, file)
            all_data.extend(parse_qa_file(path))

    # 🔥 Embed question + answer together (better semantic coverage)
    documents = [
        item["question"] + " " + item["answer"]
        for item in all_data
    ]

    embeddings = model.encode(documents)
    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index
    faiss.write_index(index, INDEX_PATH)

    # Save metadata
    with open(META_PATH, "wb") as f:
        pickle.dump(all_data, f)

    print(f"FAISS index built successfully with {len(all_data)} Q&A pairs.")
