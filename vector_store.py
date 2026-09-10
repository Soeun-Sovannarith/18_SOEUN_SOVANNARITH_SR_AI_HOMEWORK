import os
import shutil

os.environ["ANONYMIZED_TELEMETRY"] = "False"

try:
    import posthog

    posthog.capture = lambda *args, **kwargs: None
except (ImportError, AttributeError):
    pass

import chromadb
from chromadb.config import Settings

from chunking import DocumentChunk
from embeddings import get_embedding

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "school_documents"


class ChromaVectorStore:
    """Persistent Chroma store for document chunks and their embeddings."""

    def __init__(
        self,
        db_path: str = CHROMA_DB_PATH,
        collection_name: str = COLLECTION_NAME,
    ) -> None:
        self.db_path = db_path
        self.collection_name = collection_name
        self._init_collection()

    def _init_collection(self) -> None:
        try:
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(anonymized_telemetry=False),
            )
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        except Exception:
            # Clear system cache and recreate cleanly if schema migration or corruption occurs
            try:
                from chromadb.api.client import SharedSystemClient

                SharedSystemClient.clear_system_cache()
            except Exception:
                pass
            if os.path.exists(self.db_path):
                shutil.rmtree(self.db_path, ignore_errors=True)
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(anonymized_telemetry=False),
            )
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )

    def reset(self) -> None:
        """Remove indexed chunks so a fresh ingestion cannot leave stale data."""
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        """Embed and persist chunks in Chroma."""
        if not chunks:
            raise ValueError("Cannot add an empty list of chunks")

        self.collection.upsert(
            ids=[chunk.chunk_id for chunk in chunks],
            embeddings=[get_embedding(chunk.text) for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            metadatas=[
                {**chunk.metadata, "source": chunk.source}
                for chunk in chunks
            ],
        )

    def search(self, query: str, limit: int = 3) -> list[dict[str, object]]:
        """Return the closest chunks with their cosine distances."""
        if not query.strip():
            raise ValueError("query must not be blank")
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        result = self.collection.query(
            query_embeddings=[get_embedding(query)],
            n_results=limit,
            include=["documents", "metadatas", "distances"],
        )
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        return [
            {
                "text": document,
                "metadata": metadata or {},
                "distance": distance,
            }
            for document, metadata, distance in zip(
                documents, metadatas, distances, strict=False
            )
        ]
