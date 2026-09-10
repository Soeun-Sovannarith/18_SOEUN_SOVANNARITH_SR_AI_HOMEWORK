from collections.abc import Iterator
from dataclasses import dataclass

from generator import generate_answer, stream_answer
from retriever import RetrievedChunk, Retriever


@dataclass(frozen=True)
class PipelineResult:
	question: str
	answer: str
	retrieved_chunks: list[RetrievedChunk]


def answer_question_stream(
	question: str,
	retriever: Retriever,
	distance_threshold: float = 0.50,
) -> tuple[Iterator[str], list[RetrievedChunk]]:
	"""Run retrieval first, then yield answer tokens as they are generated."""
	if not question.strip():
		raise ValueError("question must not be blank")

	chunks = retriever.retrieve(question)

	# Bonus Challenge 4: Simple check if no chunk is a strong match
	if chunks and all(c.distance > distance_threshold for c in chunks):
		def _fallback_stream() -> Iterator[str]:
			yield "I could not find this in the provided documents."

		return _fallback_stream(), []

	stream = stream_answer(question, chunks)
	return stream, chunks


def answer_question(question: str, retriever: Retriever) -> PipelineResult:
	"""Run retrieval first, then generate an answer from the retrieved context."""
	if not question.strip():
		raise ValueError("question must not be blank")

	chunks = retriever.retrieve(question)
	answer = generate_answer(question, chunks)
	return PipelineResult(question, answer, chunks)
