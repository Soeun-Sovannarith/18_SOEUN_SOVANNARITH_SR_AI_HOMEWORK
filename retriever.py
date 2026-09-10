from dataclasses import dataclass

from vector_store import ChromaVectorStore


@dataclass(frozen=True)
class RetrievedChunk:
	text: str
	source: str
	distance: float
	metadata: dict[str, object]


class Retriever:
	"""Retrieve the most relevant indexed chunks for a question."""

	def __init__(self, vector_store: ChromaVectorStore, top_k: int = 12) -> None:
		if top_k <= 0:
			raise ValueError("top_k must be greater than zero")
		self.vector_store = vector_store
		self.top_k = top_k

	def retrieve(self, question: str) -> list[RetrievedChunk]:
		results = self.vector_store.search(question, limit=self.top_k)
		return [
			RetrievedChunk(
				text=str(result["text"]),
				source=str(result["metadata"].get("source", "unknown")),
				distance=float(result["distance"]),
				metadata=dict(result["metadata"]),
			)
			for result in results
		]
