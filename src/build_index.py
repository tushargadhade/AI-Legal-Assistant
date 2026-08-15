import pandas as pd
import joblib

from rank_bm25 import BM25Okapi

CSV_PATH = "data/chunks.csv"
INDEX_PATH = "data/bm25_index.pkl"


def preprocess(text):
    """
    Convert text into lowercase words.
    """

    text = str(text).lower()

    # Simple tokenization
    tokens = text.split()

    return tokens


def build_index():

    print("Loading legal chunks...")

    # Load CSV
    df = pd.read_csv(CSV_PATH)

    print(f"Loaded {len(df)} legal chunks.")

    # Tokenize legal text
    tokenized_chunks = []

    for text in df["text"]:

        tokens = preprocess(text)

        tokenized_chunks.append(tokens)

    print("Text preprocessing completed.")

    # Create BM25 index
    bm25 = BM25Okapi(tokenized_chunks)

    print("BM25 index created.")

    # Store BM25 and original data
    index_data = {
        "bm25": bm25,
        "data": df
    }

    # Save using Joblib
    joblib.dump(index_data, INDEX_PATH)

    print()
    print("===================================")
    print("BM25 INDEX CREATED SUCCESSFULLY")
    print("===================================")
    print(f"Index saved at: {INDEX_PATH}")


if __name__ == "__main__":
    build_index()