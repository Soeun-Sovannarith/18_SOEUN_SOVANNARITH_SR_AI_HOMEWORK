import argparse

from chunking import chunk_documents
from generator import FALLBACK_RESPONSE
from ingestion import load_documents
from pipeline import answer_question_stream
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
	return Retriever(vector_store=vector_store, top_k=3)


def main() -> None:
	parser = argparse.ArgumentParser(description="Chat with local school documents")
	parser.add_argument("--data", default="data", help="Directory containing documents")
	parser.add_argument("--db", default="chroma_db", help="Persistent Chroma directory")
	parser.add_argument(
		"--hide-chunks",
		action="store_true",
		help="Hide retrieved chunk contents before the answer",
	)
	args = parser.parse_args()

	try:
		retriever = build_index(args.data, args.db)
	except Exception as error:
		raise SystemExit(f"Startup failed: {error}") from error

	show_chunks = not args.hide_chunks
	print("Ask a question about the documents. Type 'exit' to quit.")
	while True:
		question = input("\nYou: ").strip()
		if question.lower() in {"exit", "quit"}:
			print("Goodbye.")
			break
		if not question:
			print("Please enter a question.")
			continue

		if question == "/chunks":
			show_chunks = not show_chunks
			print(f"Chunk preview before answer is now: {'[ENABLED]' if show_chunks else '[DISABLED]'}")
			continue

		try:
			retrieved = retriever.retrieve(question)

			# Print retrieved chunks to the screen before printing the answer
			if show_chunks and retrieved:
				print("\n--- Retrieved Chunks ---")
				for i, chunk in enumerate(retrieved, start=1):
					print(f"[{i}] Source: {chunk.source} (distance={chunk.distance:.3f})")
					print(f"{chunk.text.strip()}\n")
				print("-" * 40)

			stream, chunks = answer_question_stream(question, chunks=retrieved)
			print("\nAssistant: ", end="", flush=True)
			full_answer: list[str] = []
			for token in stream:
				print(token, end="", flush=True)
				full_answer.append(token)
			print()

			answer_text = "".join(full_answer).strip()
			if chunks and FALLBACK_RESPONSE not in answer_text:
				print("\nReferences:")
				for number, chunk in enumerate(chunks, start=1):
					print(f"{number}. {chunk.source} (distance={chunk.distance:.3f})")
		except Exception as error:
			print(f"Unable to answer the question: {error}")


if __name__ == "__main__":
	main()

