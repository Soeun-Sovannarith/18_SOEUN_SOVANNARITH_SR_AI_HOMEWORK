from typing import List

import ollama
from pydantic import BaseModel, Field, field_validator


class EmbeddingInput(BaseModel):
    text: str = Field(min_length=1)
    model: str = Field(default="mxbai-embed-large", min_length=1)

    @field_validator("text", "model")
    @classmethod
    def reject_blank_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value must not be blank")
        return value


def get_embedding(text: str, model: str = "mxbai-embed-large") -> List[float]:
    validated_input = EmbeddingInput(text=text, model=model)

    try:
        response = ollama.embed(
            model=validated_input.model,
            input=validated_input.text,
        )
        return response
    except Exception as e:
        print(f"Error and unable to do embedding because of {e}")
        return []

