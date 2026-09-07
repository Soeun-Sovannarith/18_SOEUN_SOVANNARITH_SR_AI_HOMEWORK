from ingestion import load_documents


def main() -> None:
	collection = load_documents()
	print(f"Loaded {len(collection.documents)} documents from the data folder.")
	for document in collection.documents:
		print(f"- {document.source} ({document.file_type})")


if __name__ == "__main__":
	main()
