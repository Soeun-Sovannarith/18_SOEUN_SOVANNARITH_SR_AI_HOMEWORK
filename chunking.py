from typing import Any

from pydantic import BaseModel, Field

from ingestion import IngestedDocument


class DocumentChunk(BaseModel):
	"""A small searchable section of a source document."""

	chunk_id: str = Field(min_length=1)
	document_id: str = Field(min_length=1)
	source: str = Field(min_length=1)
	text: str = Field(min_length=1)
	metadata: dict[str, Any] = Field(default_factory=dict)


def split_document(
	document: IngestedDocument,
	chunk_size: int = 800,
	overlap: int = 120,
) -> list[DocumentChunk]:
	"""Split a document on paragraph boundaries, then wrap long paragraphs."""
	if chunk_size <= 0:
		raise ValueError("chunk_size must be greater than zero")
	if overlap < 0 or overlap >= chunk_size:
		raise ValueError("overlap must be non-negative and smaller than chunk_size")

	paragraphs = [paragraph.strip() for paragraph in document.content.split("\n\n")]
	chunks: list[DocumentChunk] = []
	chunk_number = 0

	for paragraph in paragraphs:
		if not paragraph:
			continue
		for part in _split_long_text(paragraph, chunk_size, overlap):
			chunks.append(
				DocumentChunk(
					chunk_id=f"{document.document_id}-{chunk_number}",
					document_id=document.document_id,
					source=document.source,
					text=part,
					metadata={
						**document.metadata,
						"document_id": document.document_id,
						"chunk_number": chunk_number,
					},
				)
			)
			chunk_number += 1

	return chunks


def chunk_documents(
	documents: list[IngestedDocument],
	chunk_size: int = 800,
	overlap: int = 120,
) -> list[DocumentChunk]:
	"""Chunk every ingested document with one consistent strategy."""
	chunks: list[DocumentChunk] = []
	for document in documents:
		chunks.extend(split_document(document, chunk_size, overlap))
	return chunks


def _split_long_text(text: str, chunk_size: int, overlap: int) -> list[str]:
	if len(text) <= chunk_size:
		return [text]

	parts: list[str] = []
	start = 0
	while start < len(text):
		end = min(start + chunk_size, len(text))
		if end < len(text):
			whitespace = text.rfind(" ", start, end)
			if whitespace > start:
				end = whitespace

		part = text[start:end].strip()
		if part:
			parts.append(part)

		if end >= len(text):
			break
		start = max(end - overlap, start + 1)

	return parts
