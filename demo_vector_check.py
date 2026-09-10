from chunking import chunk_documents
from ingestion import load_documents
from vector_store import ChromaVectorStore


def main() -> None:
    """Build the index and print the top three matches for one test question."""
    collection = load_documents("data")
    chunks = chunk_documents(collection.documents)
    store = ChromaVectorStore()
    store.reset()
    store.add_chunks(chunks)

    question = "What are the library borrowing rules?"
    print(f"Question: {question}\n")
    for number, result in enumerate(store.search(question, limit=3), start=1):
        print(f"{number}. {result['metadata'].get('source')}")
        print(result["text"])
        print(f"Distance: {result['distance']:.3f}\n")


if __name__ == "__main__":
    main()