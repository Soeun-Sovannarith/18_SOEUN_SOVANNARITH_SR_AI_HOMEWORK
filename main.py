import argparse

from chunking import chunk_documents
from ingestion import load_documents
from pipeline import PipelineResult, answer_question
from retriever import Retriever
from vector_store import ChromaVectorStore


def build_index(data_directory: str, db_path: str) -> Retriever:
	"""Load, chunk, embed, and persist the documents before chatting."""
	collection = load_documents(data_directory)
	if not collection.documents:
		raise ValueError(f"No .txt, .md, or .pdf documents found in {data_directory}")

	chunks = chunk_documents(collection.documents)
	vector_store = ChromaVectorStore(db_path=db_path)
	vector_store.reset()
	vector_store.add_chunks(chunks)

	print(
		f"Indexed {len(collection.documents)} documents into {len(chunks)} chunks."
	)
	return Retriever(vector_store)


def print_result(result: PipelineResult) -> None:
	print(f"\nAssitant: {result.answer}")
	if result.retrieved_chunks:
		print("\nReferences:")
		for number, chunk in enumerate(result.retrieved_chunks, start=1):
			print(f"{number}. {chunk.source} (distance={chunk.distance:.3f})")


def main() -> None:
	parser = argparse.ArgumentParser(description="Chat with local school documents")
	parser.add_argument("--data", default="data", help="Directory containing documents")
	parser.add_argument("--db", default="chroma_db", help="Persistent Chroma directory")
	args = parser.parse_args()

	try:
		retriever = build_index(args.data, args.db)
	except Exception as error:
		raise SystemExit(f"Startup failed: {error}") from error

	print("Ask a question about the documents. Type 'exit' to quit.")
	while True:
		question = input("\nYou: ").strip()
		if question.lower() in {"exit", "quit"}:
			print("Goodbye.")
			break
		if not question:
			print("Please enter a question.")
			continue

		try:
			print_result(answer_question(question, retriever))
		except Exception as error:
			print(f"Unable to answer the question: {error}")


if __name__ == "__main__":
	main()
