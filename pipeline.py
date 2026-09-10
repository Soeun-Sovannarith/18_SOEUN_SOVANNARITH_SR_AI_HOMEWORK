from dataclasses import dataclass

from generator import generate_answer
from retriever import RetrievedChunk, Retriever


@dataclass(frozen=True)
class PipelineResult:
	question: str
	answer: str
	retrieved_chunks: list[RetrievedChunk]


def answer_question(question: str, retriever: Retriever) -> PipelineResult:
	"""Run retrieval first, then generate an answer from the retrieved context."""
	if not question.strip():
		raise ValueError("question must not be blank")

	chunks = retriever.retrieve(question)
	answer = generate_answer(question, chunks)
	return PipelineResult(question, answer, chunks)
