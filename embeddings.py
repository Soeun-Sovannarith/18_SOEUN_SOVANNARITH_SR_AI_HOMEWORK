from typing import List

import ollama
from pydantic import BaseModel, Field, field_validator


class EmbeddingInput(BaseModel):
    text: str = Field(min_length=1)
    model: str = Field(default="nomic-embed-text", min_length=1)

    @field_validator("text", "model")
    @classmethod
    def reject_blank_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value must not be blank")
        return value


def get_embedding(text: str, model: str = "nomic-embed-text") -> List[float]:
    validated_input = EmbeddingInput(text=text, model=model)

    try:
        response = ollama.embed(
            model=validated_input.model,
            input=validated_input.text,
        )
        embedding = response.embeddings[0]
        return embedding

    except Exception as error:
        raise RuntimeError(
            f"Unable to create an embedding. Is Ollama running with "
            f"'{validated_input.model}' pulled? Original error: {error}"
        ) from error

