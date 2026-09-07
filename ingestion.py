from hashlib import sha256
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator
from pypdf import PdfReader


SupportedFileType = Literal["pdf", "md", "txt"]


class IngestedDocument(BaseModel):
	"""Normalized document record consumed by the RAG pipeline."""

	document_id: str = Field(min_length=1)
	source: str = Field(min_length=1)
	file_type: SupportedFileType
	content: str = Field(min_length=1)
	metadata: dict[str, Any] = Field(default_factory=dict)

	@field_validator("source", "content")
	@classmethod
	def reject_blank_values(cls, value: str) -> str:
		value = value.strip()
		if not value:
			raise ValueError("Value must not be blank")
		return value


class DocumentCollection(BaseModel):
	"""Single centralized collection of all source documents."""

	documents: list[IngestedDocument] = Field(default_factory=list)


SUPPORTED_SUFFIXES = {".pdf", ".md", ".txt"}


def load_document(file_path: str | Path) -> IngestedDocument:
	"""Load one PDF, Markdown, or text file into the normalized document model."""
	path = Path(file_path)
	suffix = path.suffix.lower()

	if suffix not in SUPPORTED_SUFFIXES:
		supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
		raise ValueError(f"Unsupported file type '{suffix}'. Supported types: {supported}")
	if not path.is_file():
		raise FileNotFoundError(f"Document does not exist: {path}")

	if suffix == ".pdf":
		content, metadata = _read_pdf(path)
	else:
		content = path.read_text(encoding="utf-8")
		metadata = {"character_count": len(content)}

	document_id = sha256(str(path.resolve()).encode("utf-8")).hexdigest()[:16]
	result = IngestedDocument(
		document_id=document_id,
		source=str(path),
		file_type=suffix[1:],
		content=content,
		metadata={
			"filename": path.name,
			"suffix": suffix,
			**metadata,
		},
	)
	return result


def load_documents(data_directory: str | Path = "data") -> DocumentCollection:
	"""Recursively load every supported document into one centralized collection."""
	directory = Path(data_directory)
	if not directory.is_dir():
		raise NotADirectoryError(f"Data directory does not exist: {directory}")

	paths = sorted(
		path for path in directory.rglob("*")
		if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
	)
	return DocumentCollection(documents=[load_document(path) for path in paths])


def _read_pdf(path: Path) -> tuple[str, dict[str, Any]]:
	if path.stat().st_size == 0:
		raise ValueError(f"PDF document is empty: {path}")

	try:
		reader = PdfReader(str(path))
	except Exception as error:
		raise ValueError(f"Unable to read PDF document '{path}': {error}") from error

	pages = [(page.extract_text() or "").strip() for page in reader.pages]
	content = "\n\n".join(page for page in pages if page)
	if not content:
		raise ValueError(f"PDF document contains no extractable text: {path}")

	return content, {
		"page_count": len(reader.pages),
		"character_count": len(content),
	}
