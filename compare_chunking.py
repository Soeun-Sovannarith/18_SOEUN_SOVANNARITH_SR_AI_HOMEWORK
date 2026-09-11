"""Compare two text splitting strategies on the same documents.

Strategy 1: Paragraph-aware chunking (preserves paragraph boundaries, splits oversized paragraphs)
Strategy 2: Fixed-size window chunking (fixed 500-char window with 100-char overlap)
"""

from chunking import chunk_documents
from ingestion import load_documents


def main() -> None:
	collection = load_documents("data")
	print(f"Loaded {len(collection.documents)} documents from data/ directory.\n")

	# Strategy 1: Paragraph-aware chunking
	para_chunks = chunk_documents(
		collection.documents, chunk_size=800, overlap=120, strategy="paragraph"
	)
	para_lengths = [len(c.text) for c in para_chunks]
	avg_para_len = sum(para_lengths) / len(para_lengths) if para_lengths else 0

	# Strategy 2: Fixed-size window chunking
	fixed_chunks = chunk_documents(
		collection.documents, chunk_size=500, overlap=100, strategy="fixed"
	)
	fixed_lengths = [len(c.text) for c in fixed_chunks]
	avg_fixed_len = sum(fixed_lengths) / len(fixed_lengths) if fixed_lengths else 0

	# Print Summary Table
	print(f"{'Metric':<30} | {'Paragraph-Aware':<20} | {'Fixed-Window':<20}")
	print("-" * 75)
	print(f"{'Total Chunks Created':<30} | {len(para_chunks):<20} | {len(fixed_chunks):<20}")
	print(f"{'Average Chunk Length (chars)':<30} | {avg_para_len:<20.1f} | {avg_fixed_len:<20.1f}")
	print(f"{'Min Chunk Length (chars)':<30} | {min(para_lengths):<20} | {min(fixed_lengths):<20}")
	print(f"{'Max Chunk Length (chars)':<30} | {max(para_lengths):<20} | {max(fixed_lengths):<20}")
	print("-" * 75)

	# Print Comparison Samples from the same document
	target_doc = "data/school_regulations.md"
	print(f"\nSample Comparison on [{target_doc}]:")
	print("\n--- Strategy 1 Sample (Paragraph-Aware): ---")
	for i, c in enumerate(
		[c for c in para_chunks if c.source.endswith("school_regulations.md")][:2], 1
	):
		print(f"[Chunk {i}] ({len(c.text)} chars):")
		print(c.text)
		print()

	print("--- Strategy 2 Sample (Fixed-Window): ---")
	for i, c in enumerate(
		[c for c in fixed_chunks if c.source.endswith("school_regulations.md")][:2], 1
	):
		print(f"[Chunk {i}] ({len(c.text)} chars):")
		print(c.text)
		print()


if __name__ == "__main__":
	main()
