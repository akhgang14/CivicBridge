import os

from ai.gemini import GeminiAI


ALLOWED_MODELS = {
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
}


def get_ai_service(model: str):

    if model not in ALLOWED_MODELS:
        raise ValueError(
            f"Unsupported Gemini model: {model}"
        )

    return GeminiAI(model=model)