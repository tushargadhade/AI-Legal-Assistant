import joblib

from rank_bm25 import BM25Okapi


INDEX_PATH = "data/bm25_index.pkl"


def preprocess(text):
    """
    Convert text into lowercase words.
    """

    text = str(text).lower()

    # Simple tokenization
    tokens = text.split()

    return tokens


def load_index():

    print("Loading BM25 index...")

    # Load index using Joblib
    index_data = joblib.load(INDEX_PATH)

    bm25 = index_data["bm25"]
    df = index_data["data"]

    return bm25, df


def search(query, top_k=5):

    # Load BM25 index
    bm25, df = load_index()

    # Process user question
    query_tokens = preprocess(query)

    # Calculate BM25 scores
    scores = bm25.get_scores(query_tokens)

    # Sort from highest score to lowest
    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    results = []

    # Get Top K results
    for index in ranked_indices[:top_k]:

        row = df.iloc[index]

        result = {
            "act": row["act"],
            "section": row["section"],
            "title": row["title"],
            "page": row["page"],
            "text": row["text"],
            "score": float(scores[index])
        }

        results.append(result)

    return results


def display_results(results):

    print()
    print("=" * 70)
    print("TOP RELEVANT LEGAL SECTIONS")
    print("=" * 70)

    for i, result in enumerate(results, start=1):

        print()
        print(f"RESULT {i}")
        print("-" * 70)

        print(f"BM25 Score : {result['score']:.2f}")
        print(f"Act        : {result['act']}")
        print(f"Section    : {result['section']}")
        print(f"Title      : {result['title']}")
        print(f"Page       : {result['page']}")

        print()
        print("Text:")
        print(result["text"])

    print()
    print("=" * 70)


if __name__ == "__main__":

    question = input("\nEnter your legal question: ")

    results = search(
        query=question,
        top_k=5
    )

    display_results(results)