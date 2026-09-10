# Chat with Documents: Naive RAG

This project is a local Retrieval-Augmented Generation prototype for the RAG Fundamentals Week 5 homework. It reads the school documents in `data/`, splits them into overlapping chunks, embeds those chunks with Ollama, stores them in persistent ChromaDB, retrieves relevant passages, and asks a local Llama model to answer from those passages.

## Requirements

- Python 3.12
- Poetry
- Ollama running locally
- `llama3.2` and `nomic-embed-text` pulled in Ollama

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
poetry install
```

## Run the app

From this project directory:

```bash
poetry run python main.py
```

The index is rebuilt from `data/` at startup and persisted in `chroma_db/`. Type a question, then type `exit` to quit. The application prints the answer and the retrieved source passages for transparency.

## Project stages

| File | Responsibility |
| --- | --- |
| `ingestion.py` | Loads `.txt`, `.md`, and `.pdf` files into validated document models |
| `chunking.py` | Splits documents on paragraph boundaries and wraps long paragraphs with overlap |
| `embeddings.py` | Creates vectors with `nomic-embed-text` through Ollama |
| `vector_store.py` | Persists and searches vectors in ChromaDB |
| `retriever.py` | Converts search results into typed retrieved chunks |
| `generator.py` | Builds a grounded prompt and calls `llama3.2` |
| `pipeline.py` | Connects retrieval and generation |
| `main.py` | Builds the index and runs the terminal chat loop |

## Chunking strategy

The app first keeps blank-line-separated paragraphs together, because school policies and information entries are easier to understand when their surrounding text remains intact. Paragraphs longer than 800 characters are split at word boundaries with a 120-character overlap. The overlap helps preserve meaning when an important sentence crosses a chunk boundary.

## Vector database and models

- Vector database: persistent ChromaDB using cosine distance
- Embedding model: Ollama `nomic-embed-text`
- Generation model: Ollama `llama3.2`

## Check retrieval independently

```bash
poetry run python demo_vector_check.py
```

This embeds a test question and prints the top three matching chunks before the chat interface is used.

## Submission evidence

- [test_log.md](test_log.md) contains five required questions and space for the exact local outputs.
- [reflection.md](reflection.md) contains the 150-300 word reflection.
