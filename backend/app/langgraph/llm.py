"""LLM configuration for LangGraph."""

from langchain_groq import ChatGroq
from app.core.config import settings


from typing import Optional
from pydantic import SecretStr


def get_llm(model_override: Optional[str] = None) -> ChatGroq:
    """Get the configured ChatGroq instance."""

    model_name = model_override or settings.LLM_MODEL

    return ChatGroq(
        api_key=SecretStr(settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None,
        model=model_name,
        temperature=0,  # We want deterministic extraction
        max_tokens=2048,
    )
