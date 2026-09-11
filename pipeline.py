from collections.abc import Iterator
from dataclasses import dataclass

from generator import generate_answer, stream_answer
from retriever import RetrievedChunk, Retriever


@dataclass(frozen=True)
class PipelineResult:
	question: str
	answer: str
	retrieved_chunks: list[RetrievedChunk]

# Streaming
def answer_question_stream(
	question: str,
	retriever: Retriever | None = None,
	chunks: list[RetrievedChunk] | None = None,
	distance_threshold: float = 0.50,
) -> tuple[Iterator[str], list[RetrievedChunk]]:
	"""Run retrieval first if not provided, then yield answer tokens as they are generated."""
	if not question.strip():
		raise ValueError("question must not be blank")

	if chunks is None:
		if retriever is None:
			raise ValueError("Either retriever or chunks must be provided")
		chunks = retriever.retrieve(question)

	# Simple check if no chunk is a strong match
	if chunks and all(c.distance > distance_threshold for c in chunks):
		def _fallback_stream() -> Iterator[str]:
			yield "I could not find this in the provided documents."

		return _fallback_stream(), []

	stream = stream_answer(question, chunks)
	return stream, chunks


def answer_question(
	question: str,
	retriever: Retriever | None = None,
	chunks: list[RetrievedChunk] | None = None,
) -> PipelineResult:
	"""Run retrieval first, then generate an answer from the retrieved context."""
	if not question.strip():
		raise ValueError("question must not be blank")

	if chunks is None:
		if retriever is None:
			raise ValueError("Either retriever or chunks must be provided")
		chunks = retriever.retrieve(question)

	answer = generate_answer(question, chunks)
	return PipelineResult(question, answer, chunks)

