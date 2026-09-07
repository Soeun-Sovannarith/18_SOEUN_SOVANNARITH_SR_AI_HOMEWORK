from itertools import combinations

from ingestion import load_documents


def _normalize_content(content: str) -> str:
	return " ".join(content.split())


def _preview(content: str, limit: int = 240) -> str:
	preview = " ".join(content.split())
	return preview if len(preview) <= limit else f"{preview[:limit]}..."


def main() -> None:
	collection = load_documents()
	print(f"Loaded {len(collection.documents)} documents from the data folder.")
	print("\nDocument previews:")
	for document in collection.documents:
		character_count = len(document.content)
		print(f"\n- {document.source} ({document.file_type}, {character_count} characters)")
		print(f"  {_preview(document.content)}")

	print("\nContent comparison:")
	for first, second in combinations(collection.documents, 2):
		is_same = _normalize_content(first.content) == _normalize_content(second.content)
		comparison = "same after whitespace normalization" if is_same else "different"
		print(f"- {first.source} vs {second.source}: {comparison}")


if __name__ == "__main__":
	main()
