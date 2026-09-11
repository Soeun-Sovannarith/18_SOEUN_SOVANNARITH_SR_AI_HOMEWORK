# Reflection

Building this local RAG system was a great learning experience. The pipeline worked well because each step is simple and modular: loading files, splitting text into paragraphs, creating embeddings, searching with ChromaDB, and streaming answers with `llama3.2`. Showing the retrieved chunks and distance scores made it easy to see where answers came from and kept responses fast.

One challenge was that pure vector search sometimes struggles with exact keywords, like specific emails or website links. It can also separate section headers from tables when splitting by paragraphs, which confuses the model. Making sure the assistant says "I could not find this in the provided documents" instead of guessing required strict prompt rules and distance checks.

To make the system better (Advanced RAG), I would add Hybrid Search to combine keyword matching (BM25) with vector search. I would also use a Re-ranker to re-order the best chunks before passing them to the model, and keep Markdown titles attached to their paragraphs so context is never lost.